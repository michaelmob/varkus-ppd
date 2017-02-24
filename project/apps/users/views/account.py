from braces import views as braces
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django_tables2 import SingleTableView
from ..tables import ReferralTable
from ..forms import AccountForm



class AccountDetailView(braces.LoginRequiredMixin, SingleTableView, DetailView):
	"""
	Detail view for the current user.
	"""
	template_name_suffix = "_detail"
	table_class = ReferralTable


	def get_object(self):
		"""
		Returns user object.
		"""
		return self.request.user


	def get_context_data(self, **kwargs):
		"""
		Modify context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		url = reverse("signup-referral", args=(self.request.user.id,))
		context["DEFAULT_TEXT"] = mark_safe("<em>Not Specified</em>")
		context["url"] = self.request.build_absolute_uri(url)
		context["percent"] = int(self.request.user.profile.get_cut_amounts()[1] * 100)
		return context


	def get_queryset(self):
		"""
		Returns table data.
		"""
		if not hasattr(self, "object"):
			self.object = self.get_object()
		return User.objects.filter(profile__referrer=self.request.user)



class AccountUpdateView(braces.LoginRequiredMixin, SuccessMessageMixin, FormView):
	"""
	Update view for user and profile
	"""
	template_name = "users/user_update.html"
	form_class = AccountForm
	success_url = reverse_lazy("account")
	success_message = "Your details have been updated!"


	def get_initial(self):
		"""
		Return inital values for form.
		"""
		initial = super(__class__, self).get_initial()
		return self.form_class.get_initial(initial, self.request.user)


	def form_valid(self, form):
		"""
		Update personal details.
		"""
		form.save_user(self.request.user)
		return super(__class__, self).form_valid(form)