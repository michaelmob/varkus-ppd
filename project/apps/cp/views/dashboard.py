from django.shortcuts import render
from django.core.cache import cache
from django.contrib.admin.views.decorators import staff_member_required
from ...leads.models import Lead
from ...offers.models import Offer

from utils import charts as Charts
from utils import cache2


def index(request):

	# Cache Charts
	key = "charts__user_%s" % request.user.id
	chart = cache.get(key)

	if (not chart):
		leads = request.user.earnings.get_leads()
		chart = [Charts.hour_chart(leads), Charts.map_chart(leads)]
		cache.set(key, chart, 3600)

	# Cache Newest OFfers
	offers = cache2.get("newest_offers", lambda: Offer.objects.order_by('-date')[:5])

	# Cache Most Recent Leads
	leads = cache2.get("recent__user_%s" % request.user.id, lambda: Lead.objects.filter(lead_blocked=False, user=request.user).order_by("-date_time")[:5])

	return render(request, "cp/dashboard/index.html", {
		"hour_chart": chart[0],
		"map_chart": chart[1],
		"offers": offers,
		"leads": leads,
	})


@staff_member_required
def staff(request):
	return render(request, "cp/dashboard/staff.html", {})
