from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate
from ..forms import RegistrationForm



class AuthenticatedMixin(View):
	"""
	Mixin to redirect users if they are already authenticated.
	"""
	success_url = reverse_lazy("dashboard")


	def dispatch(self, *args, **kwargs):
		"""
		Redirect logged in users to the success_url.
		"""
		if self.request.user.is_authenticated:
			return redirect(self.success_url)
		return super(__class__, self).dispatch(*args, **kwargs)



class RegistrationView(AuthenticatedMixin, SuccessMessageMixin, FormView):
	"""
	View for a User's registration.
	"""
	form_class = RegistrationForm
	template_name = "registration/register.html"


	def get_success_message(self, cleaned_data):
		"""
		Return a modified success_message.
		"""
		message = "Welcome to %s! "
		if settings.INVITE_ONLY:
			message += "We'll notify you when your account is activated."
		return message % settings.SITE_NAME


	def get_context_data(self, **kwargs):
		"""
		Return context dictionary.
		"""
		context = super(__class__, self).get_context_data(**kwargs)
		context["referrer"] = self.kwargs.get("referrer", "")
		context["INVITE_ONLY"] = settings.INVITE_ONLY
		return context


	def form_valid(self, form):
		"""
		Log newly created user in.
		"""
		self.object = form.save()
		user = authenticate(
			username=form.cleaned_data["username"],
			password=form.cleaned_data["password1"]
		)
		login(self.request, user)
		return super(__class__, self).form_valid(form)