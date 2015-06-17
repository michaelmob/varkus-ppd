from django.conf import settings
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.core.urlresolvers import reverse as url_reverse
from ..models import Token


def request_access(request, token=None):
	try:
		token = Token.objects.get(unique=token)

		# Give them access
		if not token.access():
			raise

		access = True
	except:
		access = False

	if access:
		return HttpResponse(
			url_reverse(
				"%ss-unlock" % dict(settings.LOCKERS)[token.locker].lower(),
				args=[token.locker_code]
			)
		)
	else:
		return HttpResponse("0")
