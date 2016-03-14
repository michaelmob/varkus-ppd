import urllib.request
from decimal import Decimal
from random import randint

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from ..models import Conversion, Token, Deposit

from apps.lockers.fields import locker_ref_to_object
from apps.offers.models import Offer
from apps.api.views.notifications import notify


@staff_member_required
def internal(request):
	offer = request.GET.get("offer")
	token = request.GET.get("token")
	typeof = request.GET.get("typeof")
	approved = request.GET.get("approved", "1") == "1"

	obj = locker_ref_to_object(request.GET.get("obj"))
	token, created = Token.get_or_create(request, obj)

	try:
		offer = Offer.objects.get(id=offer)
	except:
		return HttpResponse("Offer does not exist")

	password = Deposit.get_by_user_id(obj.user.pk).password

	url = "https://" if request.is_secure() else "http://"
	url += request.get_host()
	url += reverse(receive, args=[password])

	values = {
		"offer": offer.offer_id,
		"payout": offer.payout,
		"ip": request.META.get("REMOTE_ADDR"),
		"token": token.unique,
		"typeof": typeof,
		"approved": 0 if approved else 1
	}

	data = urllib.parse.urlencode(values)
	data = data.encode("utf-8")

	url += "?" + data.decode("utf-8")

	return HttpResponse("<a href='{0}'>{0}</a>".format(url))


def log(request, typeof):
	# Log attempt
	try:
		with open("/tmp/postbacks.txt", "a") as f:
			f.write("{1}\t{0}\t{1}\n" % (typeof,
				request.META.get("REMOTE_ADDR"),
				request.build_absolute_uri()))
	except:
		pass


def receive(request, password=None):
	offer 			= request.GET.get("offer")
	payout 			= Decimal(request.GET.get("payout", 0))
	user_ip_address = request.GET.get("ip")
	unique			= request.GET.get("token")
	typeof			= request.GET.get("typeof", "conversion").lower()
	approved 		= request.GET.get("approved", "1") == "1" # 0 chargeback, 1 approved

	user			= None
	locker_obj		= None
	user_payout 	= 0
	referral_payout = 0
	conversion_blocked	= False

	response = {
		"success": False,
		"message": "This unauthorized attempt has been logged",
		"data": {}
	}

	# All input is not None
	if not (password and offer and payout and user_ip_address and unique):
		if settings.DEBUG:
			print(
				"\nPassword: %s\nOffer ID: %s\nPayout: %s\nUser IP: %s\nUnique Token: %s\n"
				% (password, offer, payout, user_ip_address, unique))

		log(request, "DENIED")
		return JsonResponse(response)

	# Password is correct
	deposit = Deposit.get_by_password(password)
	if not deposit:
		if settings.DEBUG:
			response["debug"] = "Postback Password is incorrect"
		log(request, "DENIED")
		return JsonResponse(response)

	# Log Access
	log(request, "GRANTED")

	# Get Offer
	offer = Offer.get_by_offer_id(offer)

	# Retrieve token
	token = Token.objects.filter(unique=unique).first()

	# Token does not exist
	if not token:
		response["debug"] = "Token does not exist"
		return JsonResponse(response)

	# Make sure we don't already have a conversion
	# so we don't give double the payment
	if not settings.DEBUG and token.conversion:
		response["success"] = True
		response["message"] = "Already received"
		return JsonResponse(response)

	# Add earnings to user and locker object
	cut_amount = 0

	# If locker object exists and if user exists
	if token.locker:
		try:
			user = token.locker.user
		except:
			user = None

		# If user exists and conversion is approved
		if user and approved:
			# If offer country is in the country_block of the locker object
			if offer:
				if offer.flag in token.locker.country_block:
					conversion_blocked = True
					response["debug"] = "Country block"

			# If conversion_block chance is hit, then block the conversion
			if token.locker.conversion_block > 0:
				if randint(0, 100) <= (token.locker.conversion_block * 100):
					conversion_blocked = True
					response["debug"] = "Conversion block"

			# If the conversion wasn't conversionblocked and the type is "Conversion" (as opposed to Staff or Paid)
			if not conversion_blocked and typeof == "conversion":
				try:
					cut_amount = Decimal(user.profile.party.cut_amount)
				except:
					cut_amount = Decimal(settings.DEFAULT_CUT_AMOUNT)

				# Locker Object
				token.locker.earnings.add(payout, cut_amount, True)

				# Add Earnings to User
				user_payout = user.earnings.add(payout, cut_amount, True)

				# Referral User Object
				if user.profile.referrer:
					referral_payout = user.profile.referrer.referral_earnings.difference(
						user_payout, user.profile.party.referral_cut_amount, False)

		if user:
			# Add Conversion Notification
			user.profile.notification_conversion += 1
			user.profile.save()

		# Add earnings to offer
		if offer:
			offer.earnings.add(payout, cut_amount, typeof == "conversion")
		elif settings.DEBUG:
			response["debug"] = "Offer does not exist"

	# Set token as a conversion
	if typeof == "staff":
		token.staff = True
		conversion_blocked = True
	elif typeof == "paid":
		token.paid = True
	else:
		token.conversion = True

	token.save()

	# Create Conversion
	conversion = Conversion.create(
		offer				= offer,
		token				= token,
		user				= user,
		locker				= token.locker,
		access_url			= request.build_absolute_uri(),
		sender_ip_address	= request.META.get("REMOTE_ADDR"),
		user_ip_address		= user_ip_address,
		payout 				= payout,
		dev_payout 			= payout - user_payout,
		user_payout 		= user_payout,
		referral_payout 	= referral_payout,
		conversion_blocked		= conversion_blocked,
		deposit 			= deposit.code,
		approved 			= approved
	)

	response["success"] = True
	response["message"] = "Postback received"
	response["data"]["approved"] = approved
	response["data"]["type"] = typeof

	try:
		locker_ref = token.locker.get_type() + str(token.locker.id)
		user_ref = user.__class__.__name__ + str(user.id)

		# cache.delete_many with memcached doesn't work
		cache_keys = (
			# User Charts
			"lc_" + user_ref,
			"mc_" + user_ref,

			# Locker Charts
			"lc_" + locker_ref,
			"mc_" + locker_ref
		)

		cache.delete_many(cache_keys)
	except:
		pass

	# Clear Caches
	cache_keys = (
		"charts__offer_%s" % offer.id,
		"token__%s" % token.unique,
	)

	cache.delete_many(cache_keys)
	return JsonResponse(response)