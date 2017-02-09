from braces import views as braces
from django_tables2 import SingleTableView, RequestConfig
from django.core.management import call_command
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from axes.models import AccessLog
from billing.models import Invoice
from tickets.models import Thread
from ..tables import UserStaffTable, AccessLogStaffTable



class UserStaffuserMixin(braces.LoginRequiredMixin, braces.StaffuserRequiredMixin):
	"""
	Mixin allowing only Staff users to access page.
	"""
	model = User



class UserStaffListView(UserStaffuserMixin, SingleTableView):
	"""
	List users for Staff user.
	"""
	template_name = "staff/user_staff_list.html"
	table_class = UserStaffTable


	def get_queryset(self):
		"""
		Returns users queryset.
		"""
		return User.objects.all().prefetch_related("earnings")



class UserStaffDetailView(braces.AjaxResponseMixin, UserStaffuserMixin, DetailView):
	"""
	Detailed user view for Staff user.
	"""
	template_name = "staff/user_staff_detail.html"


	def get_ajax(self, request, *args, **kwargs):
		"""
		API for Staff users.
		"""
		action = self.request.GET.get("action")
		success = False

		if action == "recalculate":
			call_command("recalculateuser", self.get_object().pk)
			success = True

		return JsonResponse({
			"success": success
		})


	def get_context_data(self, *args, **kwargs):
		"""
		Extend context dictionary.
		"""
		context = super(__class__, self).get_context_data(*args, **kwargs)

		context["invoice_count"] = (
			Invoice.objects
				.filter(user=self.object)
				.filter(Q(paid=False) | Q(error=True))
				.count()
		)

		context["ticket_count"] = (
			Thread.objects
				.filter(user=self.object)
				.filter(last_user__is_staff=False)
				.count()
		)

		context["access_log_table"] = AccessLogStaffTable(
			AccessLog.objects
				.filter(username=self.object.username)
				.order_by("-attempt_time")
		)

		RequestConfig(
			self.request, paginate={"per_page": 5}
		).configure(context["access_log_table"])

		return context