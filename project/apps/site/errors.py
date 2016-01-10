from django.shortcuts import render


def _400(request):
	return render(request, "errors/400.html")


def _403(request):
	return render(request, "errors/403.html")


def _404(request):
	return render(request, "errors/404.html")


def _500(request):
	return render(request, "errors/500.html")