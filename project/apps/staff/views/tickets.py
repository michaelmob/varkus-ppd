from braces import views as braces
from django_tables2 import SingleTableView
from tickets.models import Thread
from ..tables import TicketStaffTable



class TicketStaffuserMixin(braces.LoginRequiredMixin, braces.StaffuserRequiredMixin):
	"""
	Mixin allowing only Staff users to access page.
	"""
	model = Thread



class TicketStaffListView(TicketStaffuserMixin, SingleTableView):
	"""
	List Tickets for Staff user.
	"""
	template_name = "staff/ticket_staff_list.html"
	table_class = TicketStaffTable


	def get_queryset(self):
		"""
		Returns users queryset.
		"""
		try:
			kwargs = {"user": int(self.request.GET.get("user_id"))}
		except:
			kwargs = {}

		return (
			Thread.objects
				.filter(**kwargs)
				.order_by("-staff_unread")
				.prefetch_related("user")
		)