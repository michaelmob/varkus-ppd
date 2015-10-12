from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect as _redirect

from apps.lockers.utils import Locker_Object
from apps.leads.models import Token, Deposit

from ..models import Offer


def redirect(request, id=None):
	try:
		# Retrieve offer if ID is an integer
		int(id)
		offer = Offer.objects.get(pk=id)
		
		# Get from previous page that set the "locker_object" variable
		# contains (locker_name, id, code)
		obj = request.session["locker_object"]
		obj = Locker_Object(*obj)

		'''# Use HTTP_REFERER to verify locker_object is correct one
		# and the guest didn't click a different link and then try
		# to complete one of these surveys for the wrong locker
		referrer = request.META.get("HTTP_REFERER")

		if referrer:
			referrer_uri = referrer.split("/")[3:]
			# obj[1] == code, so if code is in the split referrer string
			# then what we need to do is see if we can find the locker obj
			# that's in the referrer link
			if not (obj[2] in referrer_uri):
				return _redirect(referrer)'''


		token, created = Token.get_or_create(request, obj)

		print(token)
	
	except Offer.DoesNotExist:
		return _redirect(request.META.get("HTTP_REFERER", "home"))

	except Token.DoesNotExist:
		# Offer doesn't exist
		return _redirect("home")

	# Check if there's an Affiliate ID override in settings.py
	try:
		user = obj.user
		aff_id = Deposit.get_by_user_id(user.pk).aff_id
	except:
		aff_id = settings.DEFAULT_AFFILIATE_ID

	# Increment offer and user's clicks
	try:
		if created:
			offer	.earnings.increment()
			obj		.earnings.increment()
			user	.earnings.increment()
	except:
		pass

	url = str(offer.tracking_url)					\
			.replace("{o}", str(offer.offer_id))	\
			.replace("{a}", str(aff_id))			\
			.replace("{u}", str(token.unique))

	return _redirect(url)
