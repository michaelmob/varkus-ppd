from decimal import Decimal

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

from offers.models import Offer
from ..models import Conversion, Token, Deposit


def receive_payload(request, password):
	"""
	Create Conversion and modify the Token accordingly.
		* offer_conversion_signal -> adds earnings to offer
		* user_conversion_signal -> adds earnings to user
		* locker_conversion_signal -> adds earnings to locker
		* unlock_signal -> sends session (the client) message it's unlocked
		* notify_conversion_signal -> sends user message conversion received
		* clear_chart_cache_signal -> clears cache for charts
	"""
	offer_id	= request.GET.get("offer")
	payout 		= request.GET.get("payout")
	ip_address	= request.GET.get("ip")
	unique		= request.GET.get("unique")
	is_approved = request.GET.get("approved", "1") == "1"
	is_blocked 	= False

	response = {
		"success": False,
		"message": "Access denied",
		"data": { }
	}

	# Check for all arguments
	if not (offer_id and payout and ip_address and unique):
		if settings.DEBUG:
			response["data"]["debug"] = "Missing argument(s)"
		return JsonResponse(response)

	# Validate arguments
	try:
		offer_id = int(offer_id)
		payout = Decimal(payout)
	except Exception as e:
		if settings.DEBUG:
			response["data"]["debug"] = "Invalid argument(s) -- %s" % str(e)
		return JsonResponse(response)

	# Validate deposit
	deposit = Deposit.get_by_password(password)

	if not deposit:
		if settings.DEBUG:
			response["data"]["debug"] = "Deposit password not found"
		return JsonResponse(response)

	# Get offer and token
	offer = Offer.objects.filter(offer_id=offer_id).first()
	token = Token.objects.filter(unique=unique).first()

	# Modify token
	if token:
		token.unlocked = True
		token.save()

	# Conversion Block
	if offer and token and (offer.country in token.locker.country_block):
			is_blocked = True
			if settings.DEBUG:
				response["data"]["debug"] = "Country block"

	if token and token.locker.conversion_block > 0:
		if randint(0, 100) <= (token.locker.conversion_block * 100):
			is_blocked = True
			if settings.DEBUG:
				response["data"]["debug"] = "Conversion block"

	# Create conversion object
	conversion, created = Conversion.objects.get_or_create_conversion(
		token 		= token,
		offer 		= offer,
		payout  	= payout,
		sender 		= request.META.get("REMOTE_ADDR"),
		deposit		= deposit.code,
		is_approved	= is_approved,
		is_blocked	= is_blocked
	)

	# Update response
	response.update({
		"success": True,
		"message": "Notification accepted" if created else "Already accepted"
	})

	return JsonResponse(response)