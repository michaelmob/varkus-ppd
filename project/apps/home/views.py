from django.shortcuts import render, redirect
#from django.contrib import messages
from django.contrib.auth.models import User


def homepage(request):
	return render(request, "home/homepage.html", {})


def terms(request):
	return render(request, "home/terms.html", {})


def dmca(request):
	return render(request, "home/dmca.html", {})


def privacy(request):
	return render(request, "home/privacy.html", {})
