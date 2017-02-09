from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def homepage(request):
	return render(request, "site/homepage.html")


def terms(request):
	return render(request, "site/terms.html")


def dmca(request):
	return render(request, "site/dmca.html")


def privacy(request):
	return render(request, "site/privacy.html")
