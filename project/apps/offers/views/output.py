from django.shortcuts import render


def public(request, locker=None, code=None):
	'''item = output.Locker_Object("List", "uj4du")

	offers_token = output.offer_token_request_cache(
		request, item, int(request.GET.get("count")), 0.01
	)'''

	return render(
		request,
		"offers/widget/external.html",
		{
			# "offers": offers_token[0],
			# "token": offers_token[1]
		}
	)
