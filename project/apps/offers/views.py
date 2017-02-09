from braces import views as braces
from django_tables2 import SingleTableMixin, SingleTableView
from django.conf import settings
from django.views import View
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.http import HttpResponse
from conversions.models import Conversion, Boost
from controlpanel.views.generic import ActivityChartView
from .utils.sync import adgate_sync
from .models import Offer
from .tables import OfferTable, OfferConversionsTable



class OfferSyncView(braces.StaffuserRequiredMixin, braces.JSONResponseMixin, View):
	"""
	Staff-user view to manually sync offers.
	"""
	def get_ajax(self, request, *args, **kwargs):
		"""
		Returns JSON response.
		"""
		return self.render_json_response(adgate_sync())


	def get(self, request, *args, **kwargs):
		"""
		Also returns JSON response.
		"""
		return self.get_ajax(request, *args, **kwargs)



class OfferListView(braces.LoginRequiredMixin, SingleTableView):
	"""
	View to list all offers.
	"""
	model = Offer
	table_class = OfferTable
	table_pagination = {
		"per_page": settings.ITEMS_PER_PAGE_LARGE
	}


	def get_table(self):
		"""
		Add `cut_amount` variable to table.
		Returns table.
		"""
		table = super(__class__, self).get_table()
		table.cut_amount = self.request.user.profile.party.cut_amount
		return table


	def get_table_data(self):
		"""
		Table's data may include a query.
		Returns table data.
		"""
		query = self.request.GET.get("q")
		data = Offer.objects.filter(earnings_per_click__gt=0.01)

		if query:
			if query.isdigit():
				data = data.filter(pk=query)

			else:
				data = data.filter(
					Q(name__icontains=query) | Q(anchor__icontains=query)
				)

		return data


	def get_context_data(self, **kwargs):
		"""
		Modify context data.
		Returns context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["query"] = self.request.GET.get("q")
		boost_ids = Boost.objects.filter(user=self.request.user).values_list("offer_id")
		context["boosted_offers"] = Offer.objects.filter(pk__in=boost_ids)
		return context



class OfferDetailView(braces.LoginRequiredMixin, SingleTableMixin, DetailView):
	"""
	View to display specific offer in detail.
	"""
	model = Offer
	table_class = OfferConversionsTable


	def get_table_data(self, **kwargs):
		"""
		Returns queryset of data for the table.
		"""
		return (
			Conversion.objects
				.filter(offer=self.object, user=self.request.user, is_blocked=False)
				.order_by("-datetime")
		)


	def get_context_data(self, *args, **kwargs):
		"""
		Extend context dictionary.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)
		boost = Boost.objects.filter(user=self.request.user, offer=self.object).first()
		context["boost"] = boost.count if boost else 0
		return context



class OfferActivityChartView(braces.CsrfExemptMixin, braces.LoginRequiredMixin, ActivityChartView):
	"""
	View to output offer activity in JSON format.
	"""
	model = Offer



class OfferAjaxView(braces.CsrfExemptMixin, braces.LoginRequiredMixin, braces.JSONResponseMixin, DetailView):
	"""
	View for Ajax requests.
	"""
	model = Offer


	def get(self, request, **kwargs):
		"""
		Ajax API to display offer data.
		Returns JSON response.
		"""
		return self.render_json_response({})


	def post(self, request, **kwargs):
		"""
		Ajax API to modify minor things.
		Returns JSON response.
		"""
		self.action = kwargs.get("action", "").lower()
		self.object = self.get_object()

		self.response = {
			"success": True,
			"message": None,
			"data": {}
		}

		if self.action == "boost":
			self.boost()
			self.response["message"] = "This offer's has been boosted."

		elif self.action == "reset":
			self.reset_boost()
			self.response["message"] = "This offer's boost has been reset."

		elif self.action == "priority":
			self.set_priority()

		else:
			self.response["success"] = False
			self.response["message"] = "Invalid action."


		return self.render_json_response(self.response)


	def boost(self):
		"""
		Called if action is "boost", used to boost an offer.
		"""
		boost = Boost.objects.create_boost(self.request.user, self.object, 10)
		self.response["data"]["count"] = boost.count


	def reset_boost(self):
		"""
		Called if action is "reset_boost", used to reset boost by deleting it.
		"""
		Boost.objects.filter(user=self.request.user, offer=self.object).delete()


	def set_priority(self):
		"""
		Called if action is "priority", used to set an offer's priority.
		"""
		profile = self.request.user.profile
		value = self.request.POST.get("value")

		self.response["message"] = "This offer's priority has been changed."

		profile.offer_block.remove(self.object)
		profile.offer_priority.remove(self.object)

		# Priority
		if value == "priority":
			profile.offer_priority.add(self.object)

		# Block
		elif value == "block":
			profile.offer_block.add(self.object)