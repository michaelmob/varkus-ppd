# https://github.com/sevennineteen/django-cloudflare/blob/master/middleware.py

class CFMiddleware(object):
	"""Updates REMOTE_ADDR for requests proxied through CloudFlare."""

	def __init__(self):
		self.cloudflare_ip_header = 'HTTP_CF_CONNECTING_IP'

	def has_cf_header(self, request):
		"Checks whether request has recognized CloudFlare header."
		return self.cloudflare_ip_header in request.META

	def process_request(self, request):
		"Overwwrites REMOTE_ADDR with user's real IP from CloudFlare header."
		if self.has_cf_header(request):
			request.META['REMOTE_ADDR'] = request.META[self.cloudflare_ip_header]
