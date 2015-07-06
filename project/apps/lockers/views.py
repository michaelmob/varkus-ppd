from django.shortcuts import render, redirect


def locker_404(request):
	return redirect("home")
