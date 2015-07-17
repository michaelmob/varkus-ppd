from django.shortcuts import HttpResponse

from html import unescape
from decimal import Decimal
from datetime import datetime
from json import loads
from urllib.request import urlopen

from ..models import Offer
from utils.user_agent import get_ua


def adgate(request):
	out = adgate_sync()

	return HttpResponse(
		"Added: %s | Removed: %s | Updated: %s | Untouched: %s | OKAY @ %s" %
		(
			out["added"], out["removed"], out["updated"], out["untouched"], out["date_time"]
		)
	)


def adgate_sync():
	aff_id = "43196"
	aff_key = "18527d29062f11802b2e2aea5d7b94ab"

	url = "https://api.adgatemedia.com/v1/offers?aff=%s&api_key=%s&minepc=.01&paymin=.05" % (aff_id, aff_key)
	offers_remote 	= loads(urlopen(url).read().decode("utf-8"))
	offers_local 	= Offer.objects.all()
	
	local_untouched = len(offers_local)

	# Declare
	offers_added = 0
	offers_updated = 0
	offer_ids = []

	# Add and update offers
	for offer_remote in offers_remote:
		offer_ids.append(offer_remote["id"])
		try:
			updated = False
			offer_local = offers_local.get(offer_id=offer_remote["id"])

			# Update EPCs
			if float(offer_local.earnings_per_click) != float(offer_remote["epc"]):
				offer_local.earnings_per_click = Decimal(offer_remote["epc"])
				offer_local.difference = Decimal(offer_remote["payout"]) - Decimal(offer_remote["epc"])
				updated = True
				
			# Update Payouts
			if float(offer_local.payout) != float(offer_remote["payout"]):
				offer_local.payout = Decimal(offer_remote["payout"])
				updated = True

			# We updated, so lets save
			if updated:
				offer_local.save()
				offers_updated += 1

		except Offer.DoesNotExist:
			payout = Decimal(offer_remote["payout"])
			epc = Decimal(offer_remote["epc"])

			# {o} == Offer ID
			# {a} == Aff ID
			# {u} == Unique hash

			tracking_url = str(offer_remote["tracking_url"]) 	\
				.replace("/" + str(offer_remote["id"]), "/{o}") \
				.replace("/" + str(aff_id), 			"/{a}") \
				.replace("?s1=", 						"?s1={u}")

			if payout > 0.00 and epc > 0.00:
				Offer.create(
					id=offer_remote["id"],
					name=unescape(offer_remote["name"]),
					anchor=unescape(offer_remote["anchor"]),
					requirements=unescape(offer_remote["requirements"]),
					user_agent=get_ua(offer_remote["ua"]),
					category=offer_remote["category"],
					earnings_per_click=offer_remote["epc"],
					country=offer_remote["country"],
					payout=payout,
					tracking_url=tracking_url
				)
				offers_added += 1
		
	# Remove offers
	excludes = Offer.objects.exclude(offer_id__in=offer_ids)
	offers_removed = excludes.count()
	offers_untouched = local_untouched - excludes.count()
	excludes.delete()

	# Return with data
	return {
		"added": offers_added,
		"removed": offers_removed,
		"updated": offers_updated,
		"untouched": offers_untouched,
		"date_time": str(datetime.now())
	}
