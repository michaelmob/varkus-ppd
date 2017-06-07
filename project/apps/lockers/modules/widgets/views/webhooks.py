import urllib.request
import socks
from sockshandler import SocksiPyHandler
from urllib.parse import quote_plus
from datetime import datetime
from random import randint
from django.conf import settings
from viking.utils import urls


def send_payload(object_, test=False):
	"""
	Send HTTP GET payload to the user's specified webhook URL.

	Example:
	http://varkus.com/notify/?offer_id={offer_id}&offer_name={offer_name}
		&ip={ip}&user_agent={user_agent}&token={token}&widget={widget}
		&payout={payout}&approved={approved}&date={date}&time={time}
		&datetime={datetime}&rand={rand}
	"""
	# Verify webhook URL is valid before we go any further
	if not urls.valid(object_.locker.webhook_url):
		return

	# Get Locker and Token from Conversion Object
	locker = object_.locker
	token = object_.token
	date = datetime.now()

	url = (
		str(locker.webhook_url)
			.replace("{offer_id}", str(object_.offer.pk))
			.replace("{offer_name}", quote_plus(str(object_.offer_name)))
			.replace("{ip}", str(object_.ip_address))
			.replace("{user_agent}", quote_plus(str(object_.user_agent)))
			.replace("{token}", str(token.unique))
			.replace("{widget}", str(locker.code))
			.replace("{payout}", "%.2f" % object_.payout)
			.replace("{approved}", str(object_.is_approved))
			.replace("{date}", str(date.strftime("%Y-%m-%d")))
			.replace("{time}", str(date.strftime("%H:%M:%S")))
			.replace("{datetime}", str(date.strftime("%Y-%m-%d_%H:%M:%S")))
			.replace("{rand}", str(randint(1, 1000000)))
			.replace("{test}", str(test))
	)

	# Use Proxy
	if settings.USE_PROXY:
		try:
			opener = urllib.request.build_opener(SocksiPyHandler(
				socks.SOCKS5, *settings.PROXY_SERVER, **settings.PROXY_CREDENTIALS
			))
			urllib.request.install_opener(opener)
		except:
			return False

	# Send payload
	try:
		return str(urllib.request.urlopen(url).read(), "utf-8")
	except:
		return False

	return True
