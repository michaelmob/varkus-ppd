from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.generic import edit, detail
from braces import views as braces
import django_tables2 as tables
from .models import Thread, Post
from .tables import TicketTable
from .forms import ThreadForm, PostForm



class TicketMixin(braces.LoginRequiredMixin):
	"""
	Mixin for Ticket views.
	"""
	model = Thread



class TicketListView(TicketMixin, tables.SingleTableView):
	"""
	View to display tickets owned by user in a table.
	"""
	table_class = TicketTable


	def get_table_data(self):
		"""
		Returns table data belonging to user.
		"""
		return self.model.objects.filter(user=self.request.user).order_by("closed")



class TicketCreateView(TicketMixin, edit.CreateView):
	"""
	Ticket creation view.
	"""
	form_class = ThreadForm
	template_name_suffix = "_create"


	def form_valid(self, form):
		"""
		Override .form_valid() method.
		Set 'user' field of object to be created.
		Returns value of parent's .form_valid() method.
		"""
		# Create Thread object
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.ip_address = self.request.META.get("REMOTE_ADDR")
		return super(__class__, self).form_valid(form)



class TicketDetailView(TicketMixin, braces.AjaxResponseMixin, edit.CreateView, detail.DetailView):
	"""
	Ticket detail view and post creation view.
	"""
	form_class = PostForm
	template_name_suffix = "_detail"
	no_permission_message = "You do not have permission to do that."


	def get_ajax(self, request, **kwargs):
		"""
		Allow status to be changed from Ajax request.
		"""
		result = {
			"success": True,
			"message": "Ticket status has been updated.",
			"data": {
				"status": None
			}
		}

		save = True
		self.object = self.get_object()
		action = self.kwargs.get("action")

		# Close Ticket
		if self.object and action == "close":
			result["data"]["status"] = "CLOSED"
			self.object.closed = True

		# Open Ticket
		elif self.object and action == "open":
			result["data"]["status"] = "OPEN"
			self.object.closed = False

		# Delete post
		elif self.object and self.request.POST.get("pid") and action == "delete":
			post = Post.objects.filter(
				user=self.request.user,
				thread=self.object,
				id=self.request.POST.get("pid"),
				datetime__gt=datetime.now() - timedelta(days=1)
			).first()

			if post:
				result["data"]["status"] = "DELETED"
				result["data"]["message"] = "Post has been deleted!"
				post.delete()
			else:
				result["data"]["status"] = "ERROR"
				result["data"]["message"] = "An error has occured."

			save = False

		# Unknown / Ticket not found
		else:
			result["success"] = False
			result["message"] = "Unknown action."
			save = False

		if save:
			self.object.save()

		return JsonResponse(result)


	def post_ajax(self, request, **kwargs):
		"""
		Forward to get_ajax.
		"""
		return self.get_ajax(request, **kwargs)


	def get_queryset(self, **kwargs):
		"""
		Be sure that user owns the Ticket object (or is Staff).
		"""
		result = super(__class__, self).get_queryset(**kwargs)

		if self.request.user.is_staff:
			return result

		return result.filter(user=self.request.user)


	def form_valid(self, form):
		"""
		Set user and thread for new Post.
		"""
		self.object = self.get_object()

		if self.object.user != self.request.user and not self.request.user.is_staff:
			form.add_error("message", self.no_permission_message)
			return super(__class__, self).form_invalid(form)

		# Create Post object
		if self.object:
			self.post = form.save(commit=False)
			self.post.user = self.request.user
			self.post.ip_address = self.request.META.get("REMOTE_ADDR")
			self.post.thread = self.object
			result = super(__class__, self).form_valid(form)

		# Thread not found
		else:
			form.add_error("message", self.no_permission_message)
			result = super(__class__, self).form_invalid(form)

		return result