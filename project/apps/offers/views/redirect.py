from django.shortcuts import redirect as _redirect
from django.conf import settings
from ..models import Offer
from apps.leads.models import Token, Deposit


def redirect(request, id=None, token=None):
	try:
		# Attempt to get offer
		int(id)
		offer = Offer.objects.get(pk=id)
		token = Token.objects.get(unique=token)
	except:
		# Offer doesn't exist
		return _redirect("home")

	offer.increment_clicks(request.META.get("REMOTE_ADDR"))

	# Check if there's an Affiliate ID override in settings.py
	try:
		aff_id = Deposit.get_by_user_id(token.locker_object().user.pk).aff_id
	except:
		aff_id = settings.DEFAULT_AFFILIATE_ID

	return _redirect(
		settings.OFFER_REDIRECT_URL % (
			offer.offer_id,
			aff_id,
			token.unique
		)
	)

