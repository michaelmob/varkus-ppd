from django.views.generic import TemplateView
from braces.views import CsrfExemptMixin, LoginRequiredMixin
from django_tables2.views import MultiTableMixin

from conversions.models import Conversion
from offers.models import Offer
from controlpanel.views.generic import ActivityChartView, MapChartView

from ..tables import SmallOffersTable, RecentConversionsTable



class DashboardView(MultiTableMixin, LoginRequiredMixin, TemplateView):
	"""
	Dashboard View which displays useful information to the user.
	"""
	template_name = "controlpanel/dashboard/dashboard.html"


	def get_tables(self, **kwargs):
		"""
		Returns list of tables.
		"""
		newest_offers_table = SmallOffersTable(
			Offer.objects.order_by("-date")[:5]
		)

		top_offers_table = SmallOffersTable(
			Offer.objects.filter(payout__gt=0.75).order_by("-success_rate")[:5]
		)

		recent_conversions_table = RecentConversionsTable(
			Conversion.objects.filter(user=self.request.user, is_approved=True)
				.prefetch_related("locker")
				.order_by("-datetime")[:5]
		)

		return (recent_conversions_table, newest_offers_table, top_offers_table)



class DashboardActivityChartView(CsrfExemptMixin, LoginRequiredMixin, ActivityChartView):
	"""
	Activity chart view for the user's dashboard.
	"""
	def get_object(self):
		"""
		Returns user object.
		"""
		return self.request.user



class DashboardMapChartView(MapChartView, DashboardActivityChartView):
	"""
	Map chart view for the user's dashboard.
	"""
	pass