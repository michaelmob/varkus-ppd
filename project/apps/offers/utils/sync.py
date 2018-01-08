import json
from html import unescape
from decimal import Decimal
from datetime import datetime
from urllib.request import urlopen
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from ..models import Offer


def adgate_sync():
	"""
	Offer synchronization for AdgateMedia's offers.
	"""
	url = (
		"https://api.adgatemedia.com/v1/offers"
		"?aff=%s&api_key=%s&minepc=.01&paymin=.05"
	) % (settings.ADGATE_API_ID, settings.ADGATE_API_KEY)
	offers = json.loads(urlopen(url).read().decode("utf-8"))

	start_datetime = datetime.now()

	offers_added = 0
	offers_updated = 0
	offer_ids = []  # Offers still in database

	# For each offer in adgate's response
	for offer in offers:
		# Add to offer_id, which in the end tells to exclude
		# these offers from being deleted
		offer_ids.append(offer["id"])

		# Offer details
		offer["payout"] = Decimal(offer["payout"])
		offer["epc"] = Decimal(offer["epc"])
		offer["country"] = ",".join(offer["country"]).upper()

		# {o} == Offer ID, {a} == Aff ID, {u} == Unique hash
		offer["tracking_url"] = (
			str(offer["tracking_url"])
				.replace("/" + str(offer["id"]), "/{o}")
				.replace("/" + str(settings.ADGATE_API_ID), "/{a}")
				.replace("?s1=", "?s1={u}")
		)

		try:
			obj, created = Offer.objects.update_or_create(
				offer_id = int(offer["id"]),
				defaults = {
					"name": unescape(offer["name"]),
					"anchor": unescape(offer["anchor"]),
					"requirements": unescape(offer["requirements"]),
					"user_agent": unescape(offer["ua"]),
					"category": offer["category"],
					"earnings_per_click": offer["epc"],
					"countries": offer["country"],
					"payout": offer["payout"],
					"tracking_url": offer["tracking_url"],
				}
			)
		except MultipleObjectsReturned:
			Offer.objects.filter(offer_id=int(offer["id"])).first().delete()
			continue

		if created:
			offers_added += 1
		else:
			offers_updated += 1

	# Remove old offers
	old_offers = Offer.objects.exclude(offer_id__in=offer_ids)
	offers_deleted = old_offers.count()
	old_offers.delete()

	# Return with data
	return {
		"success": True,
		"message": "Offers have been synchronized.",
		"data": {
			"added": offers_added,
			"removed": offers_deleted,
			"updated": offers_updated,
			"count": Offer.objects.all().count(),
			"elapsed": (datetime.now() - start_datetime).seconds,
			"datetime": str(datetime.now())
		}
	}
