from html import unescape
from decimal import Decimal
from datetime import datetime
from json import loads
from urllib.request import urlopen

from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.admin.views.decorators import staff_member_required

from ..models import Offer, Earnings
from utils.user_agent import format_ua

@staff_member_required
def sync(request):
	return JsonResponse(adgate_sync())


def adgate_sync():
	url = "https://api.adgatemedia.com/v1/offers?aff=%s&api_key=%s&minepc=.01&paymin=.05" % \
			(settings.ADGATE_API_ID, settings.ADGATE_API_KEY)
	offers = loads(urlopen(url).read().decode("utf-8"))

	start_datetime = datetime.now()

	# Declare
	offers_added 	= 0
	offers_updated 	= 0
	offer_ids 		= []  # Offers still in database

	# For each offer in adgate's offer api
	for offer in offers:

		# Add to offer_id, which in the end tells to exclude
		# these offers from being deleted
		offer_ids.append(offer["id"])

		# Offer vars
		payout	= Decimal(offer["payout"])
		epc 	= Decimal(offer["epc"])
		country = offer["country"].upper()

		# {o} == Offer ID, {a} == Aff ID, {u} == Unique hash
		tracking_url = str(offer["tracking_url"]) 	\
			.replace("/" + str(offer["id"]), 			"/{o}") \
			.replace("/" + str(settings.ADGATE_API_ID),	"/{a}") \
			.replace("?s1=", 							"?s1={u}")

		try:
			obj, created = Offer.objects.update_or_create(
				offer_id	= int(offer["id"]),
				defaults	= {
					"name"					: Offer.clean_name(unescape(offer["name"])),
					"anchor"				: unescape(offer["anchor"]),
					"requirements"			: unescape(offer["requirements"]),
					"user_agent"			: format_ua(offer["ua"]),
					"category"				: offer["category"],
					"earnings_per_click"	: offer["epc"],
					"country"				: country,
					"flag" 					: Offer.pick_flag(country),
					"country_count" 		: len(country.split(',')),
					"payout" 				: payout,
					"success_rate"			: float((epc / payout) * 100),
					"tracking_url" 			: tracking_url,
				}
			)
		except MultipleObjectsReturned:
			Offer.objects.filter(offer_id=int(offer["id"])).first().delete()
			continue

		if created:
			Earnings.objects.get_or_create(obj=obj)
			offers_added += 1
		else:
			offers_updated += 1

	# Remove old offers
	old = Offer.objects.exclude(offer_id__in=offer_ids)
	offers_deleted = old.count()
	old.delete()

	end_datetime = datetime.now()

	# Return with data
	return {
		"success": True,
		"message": "Synced",
		"data": {
			"added": offers_added,
			"removed": offers_deleted,
			"updated": offers_updated,
			"count": Offer.objects.all().count(),
			"elapsed": (end_datetime - start_datetime).seconds,
			"datetime": str(datetime.now())
		}
	}
