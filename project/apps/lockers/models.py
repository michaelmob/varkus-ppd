from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse

from apps.cp.models import Earnings_Base
from utils import strings

from .fields import LockerField


''' Base for Lockers '''
class Locker_Base(models.Model):
	user 			= models.ForeignKey(User)
	code 			= models.CharField(max_length=10, verbose_name="Code")
	name 			= models.CharField(max_length=100, verbose_name="Name")
	description 	= models.TextField(max_length=500, default=None, blank=True, null=True, verbose_name="Description")
	date_time 		= models.DateTimeField(auto_now_add=True, verbose_name="Date")

	theme			= models.CharField(max_length=64, default="DEFAULT", choices=settings.LOCKER_THEMES)
	offers_count	= models.IntegerField(default=8)

	lead_block		= models.DecimalField(
		validators 	 	= [MinValueValidator(0), MaxValueValidator(1)],
		max_digits 		= 5,
		decimal_places 	= 2,
		default 		= "0",
		help_text 		= """Chance of a lead block happening.<br/>
			Divide by 100 (example: 0.30 == 30%)<br/>
			1 for guaranteed lead block.<br/>
			0 for no lead block.""")

	country_block	= models.CharField(
		max_length 		= 100,
		default 		= "",
		blank 			= True,
		null 			= True,
		help_text 		= "ISO 3166-1 alpha-2 (example: \"US,FR,\")")

	def get_type(self):
		"""Get class name (Ex: widget, file, list, link)"""
		return str(self.__class__.__name__).lower()

	def get_link(self, loc):
		"""Base function to get link related to class (Ex: file-%s)"""
		return reverse(self.get_type() + "s-%s" % loc, args=(self.code,))

	def get_manage_url(self):
		"""Get manage (control panel) url (Ex: file-manage -> /files/manage/code/)"""
		return self.get_link("manage")

	def get_locker_url(self):
		"""Get locker (locker page) url (Ex: file-locker -> /file/code/)"""
		return self.get_link("locker")

	def get_unlock_url(self):
		"""Get unlock (locker page) url (Ex: file-locker -> /file/code/unlock/)"""
		return self.get_link("unlock")

	def generate_code(self, length=5):
		"""Generate unused code for locker"""
		runs = 0
		code = strings.random(length)  # generate code

		# while code is in use
		while self.__class__.objects.filter(code=code).exists():
			runs += 1

			# if ran more than twice, add one to length ("code1" -> "code12")
			if runs > 2:
				runs = 0
				length += 1

			# generate new code
			code = strings.random(length)

		return code

	def __str__(self):
		return "%s %s: %s" % (self.__class__.__name__, self.pk, self.name)

	class Meta:
		app_label = "lockers"
		abstract = True