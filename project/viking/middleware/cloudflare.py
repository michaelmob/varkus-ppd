class CFMiddleware(object):
	def process_request(self, request):
		if "HTTP_CF_CONNECTING_IP" in request.META:
			request.META['REMOTE_ADDR'] = request.META[self.cloudflare_ip_header]