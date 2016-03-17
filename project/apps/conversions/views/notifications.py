from decimal import Decimal

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

from apps.offers.models import Offer
from ..models import Conversion, Token, Deposit


def receive(request, password):
	""" Create Conversion and modify the Token accordingly
		* offer_conversion_signal -> adds earnings to offer
		* user_conversion_signal -> adds earnings to user
		* locker_conversion_signal -> adds earnings to locker
		* unlock_signal -> sends session (the client) message it's unlocked
		* notify_conversion_signal -> sends user message conversion received
		* charts_conversion_signal -> clears cache for charts
		"""
	offer_id	= request.GET.get("offer")
	payout 		= request.GET.get("payout")
	ip_address	= request.GET.get("ip")
	unique		= request.GET.get("unique")
	approved 	= request.GET.get("approved", "1") == "1"
	blocked 	= False

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
		token.conversion = True
		token.save()

	# Conversion Block
	if offer and token and (offer.flag in token.locker.country_block):
			blocked = True
			if settings.DEBUG:
				response["data"]["debug"] = "Country block"

	if token and token.locker.conversion_block > 0:
		if randint(0, 100) <= (token.locker.conversion_block * 100):
			blocked = True
			if settings.DEBUG:
				response["data"]["debug"] = "Conversion block"

	# Create conversion object
	conversion, created = Conversion.get_or_create(
		offer 				= offer,
		token 				= token,
		payout  			= payout,
		sender_ip_address 	= request.META.get("REMOTE_ADDR"),
		user_ip_address 	= ip_address,
		deposit				= deposit.code,
		approved			= approved,
		blocked				= blocked
	)

	# Update response
	response.update({
		"success": True,
		"message": "Notification accepted" if created else "Already accepted"
	})

	return JsonResponse(response)