import re
import urllib.request
import socks
from sockshandler import SocksiPyHandler
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from lockers.views.generic import LockerUnlockView



class LinkUnlockView(LockerUnlockView):
	"""
	Custom Unlock view for Link model.
	"""
	def access(self):
		"""
		Returns unlocked view. When 'download' GET argument is present then
		return the download view.
		"""
		if self.action != "view":
			return

		return self.redirect() if not self.object.proxy else self.proxy()


	def redirect(self):
		"""
		Return redirection to URL.
		"""
		return redirect(self.object.url)



	def __match(self, match):
		"""
		Determine if URL is relative, absolute, or needs no modification.
		"""
		attr, value = match.group(1), match.group(2)

		# Valid URL
		if value[:4] == "http" or value[:2] == "//":
			return match.group(0)

		# Absolute URL
		if value[:1] == "/":
			return "%s='%s'" % (attr, self.absolute_path + value)

		# Relative URL
		return "%s='%s'" % (attr, self.relative_path + value)


	def proxy(self):
		"""
		Return a proxied page request.
		"""
		if settings.USE_PROXY:
			try:
				opener = urllib.request.build_opener(SocksiPyHandler(
					socks.SOCKS5, *settings.PROXY_SERVER, **settings.PROXY_CREDENTIALS
				))
				urllib.request.install_opener(opener)
			except:
				return self.redirect()

		response = urllib.request.urlopen(self.object.url, timeout=30)
		length = response.getheader("Content-Length")

		url = urlparse(response.geturl())
		self.absolute_path = "%s://%s" % (url.scheme, url.netloc)
		self.relative_path = "/".join(self.object.url.split("/")[:-1]) + "/"

		if not (length and length.isdigit() and int(length) < 10000000):
			return self.redirect()

		html = response.read().decode("unicode_escape")
		html = re.sub(r"(src|href)=(?:\'|\")(.*?)(?:\'|\")", self.__match, html)
		return HttpResponse(html)
