import urllib.request
from decimal import Decimal
from random import randint

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from ..models import Lead, Token, Deposit
from ...offers.models import Offer


@staff_member_required
def send(request):
	offer = request.GET.get("offer")
	token = request.GET.get("token")
	typeof = request.GET.get("typeof")

	try:
		token = Token.objects.get(unique=token)
	except:
		return HttpResponse("Token does not exist.")

	try:
		offer = Offer.objects.get(id=offer)
	except:
		return HttpResponse("Offer does not exist.")

	
	password = Deposit.get_by_user_id(token.locker_object().user.pk).password

	url = "https://" if request.is_secure() else "http://"
	url += request.get_host()
	url += reverse(receive, args=[password])

	values = {
		"offer": offer.offer_id,
		"payout": offer.payout,
		"ip": request.META.get("REMOTE_ADDR"),
		"token": token.unique,
		"typeof": typeof
	}

	data = urllib.parse.urlencode(values)
	data = data.encode("utf-8")

	url += "?" + data.decode("utf-8")
	print(url)

	request2 = urllib.request.Request(url)
	response = urllib.request.urlopen(request2)

	return HttpResponse(response.read())


def receive(request, password=None):
	offer 			= request.GET.get("offer")
	payout 			= Decimal(request.GET.get("payout", 0))
	user_ip_address = request.GET.get("ip")
	token			= request.GET.get("token")
	typeof			= request.GET.get("typeof", "lead").lower()

	user			= None
	locker_obj		= None
	user_payout 	= 0
	referral_payout = 0
	lead_blocked	= False

	response = {
		"error": True,
		"message": "This unauthorized attempt has been logged."  # Sike!
	}

	# All input is not None
	if not (password and offer and payout and user_ip_address and token):
		if settings.DEBUG:
			print(
				"\nPassword: %s\nOffer ID: %s\nPayout: %s\nUser IP: %s\nToken: %s\n"
				% (password, offer, payout, user_ip_address, token)
			)
		return JsonResponse(response)

	# Password is correct
	deposit = Deposit.get_by_password(password)
	if not deposit:
		if settings.DEBUG:
			response["debug"] = "Postback Password is incorrect."
		return JsonResponse(response)

	# Get Offer
	offer = Offer.get_by_offer_id(offer)

	# Verify Token, but continue
	token = Token.get_verify(token, user_ip_address)
	if settings.DEBUG:
		if not token:
			response["debug"] = "Token does not exist."

	if token:
		# Make sure we don't already have a lead
		# so we don't give double the payment
		if token.lead:
			response["error"] = False
			response["message"] = "Already received."
			return JsonResponse(response)

		# Add earnings to user and locker object
		locker_obj = token.locker_object()

		cut_amount = 0

		if locker_obj:
			if offer:
				if offer.flag in locker_obj.country_block:
					lead_blocked = True
					response["debug"] = "Country block."

			if locker_obj.lead_block > 0:
				if randint(0, 100) <= (locker_obj.lead_block * 100):
					lead_blocked = True
					response["debug"] = "Lead block."

			if not lead_blocked:
				user = locker_obj.user
				cut_amount = user.profile.party.cut_amount

				# Locker Object
				locker_obj.earnings.add(payout, cut_amount)

				# Add Earnings to User
				user_payout = user.earnings.add(payout, cut_amount)

				# Referral User Object
				if user.profile.referrer:
					referral_payout = user.profile.referrer.referral_earnings.difference(
						user_payout, user.profile.party.referral_cut_amount, False
					)

			# Add earnings to offer
			if offer:
				offer.earnings.add(payout, cut_amount)
			elif settings.DEBUG:
				response["debug"] = "Offer does not exist."

		# Set token as a lead
		if typeof == "staff":
			token.staff = True
		elif typeof == "paid":
			token.paid = True
		else:
			token.lead = True

		token.save()

	# Create Lead
	Lead.create(
		offer				= offer,
		token				= token,
		user				= user,
		locker_obj			= locker_obj,
		sender_ip_address	= request.META.get("REMOTE_ADDR"),
		user_ip_address		= user_ip_address,
		payout 				= payout,
		dev_payout 			= payout - user_payout,
		user_payout 		= user_payout,
		referral_payout 	= referral_payout,
		lead_blocked		= lead_blocked,
		deposit 			= deposit.code
	)

	response["error"] = False
	response["type"] = typeof
	response["message"] = "Received."

	# No Locker
	try:
		locker_reference = (type(locker_obj).__name__.lower(), locker_obj.pk)

		# Clear User/Locker Cache
		cache.delete_many([
			"charts__user_%s" % user.id,
			"recent__user_%s" % user.id,
			"charts__%s_%s" % locker_reference,
			"leads__%s_%s" % locker_reference
		])
	except:
		response["user"] = None

	# Clear Caches
	cache.delete_many([
		"charts__offer_%s" % offer.id,
		"token__%s" % token.unique,
	])

	return JsonResponse(response)
