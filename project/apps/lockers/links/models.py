from datetime import datetime
from django.db import models
from ..models import Locker_Base, Earnings_Base


class Link(Locker_Base):
	url		= models.URLField(max_length=1000)

	def create(user, name, description, url):
		obj = Link.objects.create(
			user 		= user,
			code 		= Link().generate_code(),
			name 		= name,
			description	= description,
			url 		= url,
			date_time	= datetime.now()
		)

		Earnings.objects.get_or_create(obj=obj)

		return obj


class Earnings(Earnings_Base):
	obj = models.OneToOneField(Link, primary_key=True)

	class Meta:
		db_table = "links_earnings"