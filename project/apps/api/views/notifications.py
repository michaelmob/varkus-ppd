from django.conf import settings
from django.shortcuts import render, redirect
from datetime import datetime
from random import randint

import urllib.request
import socks
from sockshandler import SocksiPyHandler
from urllib.parse import quote_plus


def notify(conversion_obj, test=False):
	# offer_id 			- ID of Offer
	# offer_name 		- offer_name, url encoded
	# ip 				- IP that created token
	# user_agent 		- user agent that created token
	# token 			- Token ID
	# widget 			- widget code
	# payout			- payout
	# approved 			- True or False
	# date 				- date
	# time 				- time
	# datetime 			- datetime
	# rand 				- Random number 1-1000000
	# custom			- custom text
	# custom2			- custom text2
	# custom3			- custom text3
	# custom4			- custom text4
	# custom5			- custom text5
	# test				- test

	#http://varkus.com/notify/?offer_id={offer_id}&offer_name={offer_name}&ip={ip}&user_agent={user_agent}&token={token}&widget={widget}&payout={payout}&approved={approved}&date={date}&time={time}&datetime={datetime}&rand={rand}

	# Get Locker and Token from Conversion Object
	locker_obj = conversion_obj.locker
	token_obj = conversion_obj.token

	date = datetime.now()

	url = str(locker_obj.http_notification_url)\
		.replace("{offer_id}", 		str(conversion_obj.offer.pk))\
		.replace("{offer_name}", 	quote_plus(str(conversion_obj.offer_name)))\
		.replace("{ip}", 			str(conversion_obj.user_ip_address))\
		.replace("{user_agent}", 	quote_plus(str(conversion_obj.user_user_agent)))\
		.replace("{token}", 		str(token_obj.unique))\
		.replace("{widget}", 		str(locker_obj.code))\
		.replace("{payout}", 		str(conversion_obj.user_payout))\
		.replace("{approved}", 		str(conversion_obj.approved))\
		.replace("{date}", 			str(date.strftime("%Y-%m-%d")))\
		.replace("{time}", 			str(date.strftime("%H:%i:%S")))\
		.replace("{datetime}", 		str(date.strftime("%Y-%m-%d %H:%i:%S")))\
		.replace("{rand}", 			str(randint(1, 1000000)))\
		.replace("{test}", 			str(test))

	if settings.HTTP_NOTIFICATION_USE_PROXY:
		try:
			opener = urllib.request.build_opener(
				SocksiPyHandler(
					socks.SOCKS5,
					settings.SOCKS5_SERVER,
					settings.SOCKS5_PORT, True,
					settings.SOCKS5_USERNAME,
					settings.SOCKS5_PASSWORD
				)
			)

			urllib.request.install_opener(opener)
		except:
			print("Proxy error")
			return False

	try:
		html = str(urllib.request.urlopen(url).read(), "utf-8")
	except:
		return False

	return True



def test(request):
	pass