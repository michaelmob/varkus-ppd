from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from ..cp.models import Earnings_Base
from utils import strings


class Locker_Base(models.Model):
	user 		= models.ForeignKey(User)
	code 		= models.CharField(max_length=10)
	name 		= models.CharField(max_length=100)
	description = models.TextField(max_length=500, default="", blank=True, null=True)
	date_time 	= models.DateTimeField()

	lead_block	= models.DecimalField(
		validators 	 	= [MinValueValidator(0), MaxValueValidator(1)],
		max_digits 		= 5,
		decimal_places 	= 2,
		default 		= "0",
		help_text 		= """Chance of a lead block happening.<br/>
			Divide by 100 (example: 0.30 == 30%)<br/>
			1 for guaranteed lead block.<br/>
			0 for no lead block."""
	)

	country_block	= models.CharField(
		max_length 		= 100,
		default 		= "",
		blank 			= True,
		null 			= True,
		help_text 		= "ISO 3166-1 alpha-2 (example: \"US,FR,\")"
	)

	def generate_code(self, length=5):
		runs = 0
		code = strings.random(length)

		while self.__class__.objects.filter(code=code).exists():
			runs += 1

			if runs > 2:
				runs = 0
				length += 1

			code = strings.random(length)

		return code

	def __str__(self):
		return "%s: %s" % (self.pk, self.name)

	class Meta:
		abstract = True
