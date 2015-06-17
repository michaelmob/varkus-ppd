from django.shortcuts import redirect

def signup(request, referrer=-1):
	return redirect("signup-referral", referrer=referrer)