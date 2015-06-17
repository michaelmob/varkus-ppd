from django.shortcuts import render, redirect
#from django.contrib import messages
from django.contrib.auth.models import User


def index(request):
	return render(request, "home/index.html", {})

	
def terms(request):
	return render(request, "home/terms.html", {})
	

def dmca(request):
	#messages.error(request, "You have forgotten to enter a CAPTCHA!")
	return render(request, "home/dmca.html", {})
