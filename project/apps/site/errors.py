from django.shortcuts import render


def bad_request_400(request):
	return render(request, "errors/bad-request-400.html")


def permission_denied_403(request):
	return render(request, "errors/permission-denied-403.html")


def page_not_found_404(request):
	return render(request, "errors/page-not-found-404.html")


def internal_server_error_500(request):
	return render(request, "errors/internal-server-error-500.html")