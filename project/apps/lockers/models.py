import os.path

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.urlresolvers import reverse

from core.models import EarningsBase
from viking.utils import strings
from viking.utils.constants import DEFAULT_BLANK_NULL, BLANK_NULL



class LockerBase(models.Model):
	"""
	Base abstract model for Lockers.
	"""
	user 			= models.ForeignKey(User)
	code 			= models.SlugField(max_length=10, verbose_name="Code")
	name 			= models.CharField(max_length=100, verbose_name="Name")
	description 	= models.TextField(max_length=500, verbose_name="Description", **DEFAULT_BLANK_NULL)
	datetime 		= models.DateTimeField(auto_now_add=True, verbose_name="Date")
	theme			= models.CharField(max_length=64, default="DEFAULT", choices=settings.LOCKER_THEMES)
	offer_count		= models.IntegerField(default=8)
	conversion_block = models.DecimalField(
		validators 	 	= [MinValueValidator(0), MaxValueValidator(1)],
		max_digits 		= 5,
		decimal_places 	= 2,
		default 		= "0",
		help_text 		= (
			"Chance of a conversion block happening.<br/>"
			"Divide by 100 (example: 0.30 == 30%)<br/>"
			"0 for guaranteed conversion block.<br/>"
			"0 for no conversion block."
		)
	)
	country_block	= models.CharField(max_length=100, default="", help_text="ISO 3166-1 alpha-2 (example: \"US,FR,\")", **BLANK_NULL)


	class Meta:
		"""
		Meta class for every locker.
		"""
		app_label = "lockers"
		abstract = True


	def __str__(self):
		return "%s %s: %s" % (self.__class__.__name__, self.pk, self.name)


	@classmethod
	def maximum_amount(cls):
		"""
		Returns maximum amount of allowed objects.
		"""
		return getattr(settings, "MAX_%sS" % cls.__name__.upper())


	@property
	def type(self):
		"""
		Returns type of locker.
		"""
		return str(self.__class__.__name__).lower()


	@classmethod
	def generate_code(cls, length=5):
		"""
		Return unique code for newly created locker objects.
		"""
		runs = 0
		code = strings.random(length)  # generate code

		# while code is in use
		while cls.objects.filter(code=code).exists():
			runs += 1

			# if ran more than twice, add one to length ("code1" -> "code12")
			if runs > 2:
				runs = 0
				length += 1

			# generate new code
			code = strings.random(length)

		return code


	def save(self, *args, **kwargs):
		"""
		Override .save() method to include generated code and create earnings
		object if it does not have one.
		Returns updated class object.
		"""
		if not self.code:
			self.code = self.__class__.generate_code()

		super(__class__, self).save(*args, **kwargs)

		if not hasattr(self, "earnings") and hasattr(self, "get_earnings_model"):
			self.get_earnings_model().objects.create(parent=self)


	def filter_args(self):
		"""
		Returns dictionary of arguments for a queryset filter.
		"""
		return {
			"locker_type__pk": ContentType.objects.get_for_model(self.__class__).pk,
			"locker_id": self.id
		}


	def admin_filter_args(self):
		"""
		Returns string of GET parameters for filtering within the django admin.
		"""
		return "locker_type=%s&locker_id=%s" % (
			ContentType.objects.get_for_model(self.__class__).pk,
			self.id
		)


	def get_absolute_url(self):
		"""
		Return absolute URL for locker object.
		"""
		return reverse(self.type + "s:detail", args=(self.code,))


	def get_locker_url(self):
		"""
		Return locker URL for locker object.
		"""
		return reverse(self.type + ":lock", args=(self.code,))


	def get_unlock_url(self):
		"""
		Return unlock URL for locker object.
		"""
		return reverse(self.type + ":unlock", args=(self.code,))


	def has_css_file(self):
		"""
		Returns boolean. True if locker object has a CSS file.
		"""
		return (
			self.type == "widget" and self.css_file
				and os.path.isfile(self.css_file.path)
		)