from braces import views as braces
from django.views.generic.list import ListView
from ..models import Notification, Broadcast



class NotificationsListView(braces.LoginRequiredMixin, ListView):
	"""
	List notifications in template.
	"""
	model = Notification
	template_name = "notifications/notification_list.html"


	def get_context_data(self):
		"""
		Modify context dictionary to add the broadcast object list.
		"""
		context = super(__class__, self).get_context_data()
		context["broadcast_object_list"] = self.get_broadcast_queryset()
		return context


	def get_broadcast_queryset(self, *args, **kwargs):
		"""
		Returns broadcasts of user. Mark broadcasts as read when viewed.
		"""
		objects = Broadcast.get_broadcasts_with_unread(self.request.user)

		for object_ in objects:
			if object_.unread:
				Broadcast.mark_as_read(self.request.user, objects)
				break

		return objects


	def get_queryset(self, *args, **kwargs):
		"""
		Returns notifications of user. Mark notifications as read when viewed.
		"""
		objects = Notification.get_notifications(self.request.user)

		for object_ in objects:
			if object_.unread:
				Notification.mark_as_read(self.request.user)
				break

		return objects