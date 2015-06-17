from django.shortcuts import render


def locker_404(request):
	return render(request, "lockers/404.html", {})
