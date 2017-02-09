import os.path
from json import dumps
from datetime import datetime, timedelta
from channels import Group

from django.conf import settings
from django.db import models
from django.db.models import F
from django.core.files.base import ContentFile
from django.utils.html import escape
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from lockers.models import LockerBase, EarningsBase
from viking.utils.constants import DEFAULT_BLANK_NULL, BLANK_NULL

DEFAULTS = { "max_length": 300, "blank": True, "null": True }



class Widget(LockerBase):
	"""
	Model for Widget locker.
	"""
	locker_type 	= models.ForeignKey(ContentType, on_delete=models.SET_NULL, limit_choices_to={"app_label__in": ("lockers",)}, **BLANK_NULL)
	locker_id 		= models.PositiveIntegerField(**BLANK_NULL)
	locker 			= GenericForeignKey("locker_type", "locker_id")

	redirect_url 	= models.URLField(default=None, verbose_name="Redirect URL", **DEFAULTS)
	webhook_url 	= models.CharField(default=None, verbose_name="Webhook URL", **DEFAULTS)
	css_file 		= models.FileField(upload_to="widgets/css/", **DEFAULT_BLANK_NULL)

	viral_mode 		= models.BooleanField(default=False, verbose_name="Enable viral mode")
	viral_count 	= models.IntegerField(default=5, verbose_name="Unique visitors required")
	viral_noun		= models.CharField(default=None, verbose_name="Visitor noun (singular,plural)", **DEFAULTS)
	viral_message 	= models.CharField(default=None, verbose_name="Unsatisfied amount message", **DEFAULTS)


	@classmethod
	def get_earnings_model(cls):
		"""
		Return earnings model for Widget.
		"""
		return WidgetEarnings


	@property
	def css(self):
		"""
		Return string of custom CSS text.
		"""
		buf = None
		if self.has_css_file():
			with open(self.css_file.path, "r") as f:
				buf = "".join(f.readlines())
		return buf


	@css.setter
	def css(self, content):
		"""
		Write custom CSS file provided by user.
		"""
		if self.has_css_file() or not content:
			self.css_file.delete()
		self.css_file.save(self.code + ".css", ContentFile(content), save=True)


	def add_visitor(self, request, pk=None):
		"""
		Add visitor to WidgetVisitor for viral widgets.
		"""
		visitor, created = WidgetVisitor.objects.get_or_create(
			widget=self, ip_address=request.META.get("REMOTE_ADDR"), defaults={
				"session": request.session.session_key
			}
		)

		# Update session key
		if visitor.session != request.session.session_key:
			visitor.session = request.session.session_key
			visitor.save()

		# Add to visitor count
		if pk:
			# Look for WidgetVisitor owner
			owner = WidgetVisitor.objects.filter(pk=pk).defer("widget").first()

			# Check if owner of widgets WidgetVisitor object exists and after
			# then check that the user isn't clicking on their own link, if that
			# passes then make sure the WidgetVisitor object is not already in the
			# owners visitors list
			if (
				owner and (request.META.get("REMOTE_ADDR") != owner.ip_address)
					and not owner.visitors.filter(session=request.session.session_key).exists()
			):
				# Add to 
				owner.visitors.add(visitor)
				owner.count = F("count") + 1
				owner.save()

				# Send channels message; we cant see if a new click was added
				# in a signal...
				Group("session-" + owner.session).send({
					"text": dumps({
						"success": True,
						"type": "CLICK",
						"message": self.get_viral_message(
							WidgetVisitor.objects.filter(pk=pk).only("count").first()
						)
					})
				})

		return (visitor, created)


	def get_viral_message(self, visitor):
		"""
		Return formatted viral message.
		"""
		default_noun = "person,people"

		# Visitor names
		if not self.viral_noun or not "," in self.viral_noun:
			self.viral_noun = default_noun

		nouns = self.viral_noun.split(",")

		# Amount left
		amount = self.viral_count - visitor.count
		noun = escape(nouns[0] if amount < 2 else nouns[1])

		# User's message
		return (
			str(self.viral_message or settings.VIRAL_MESSAGE)
				.replace("{amount}", "<span id=\"amount\">%s</span>" % str(amount))
				.replace("{noun}", noun)
		)



class WidgetVisitor(models.Model):
	"""
	Model for Widget Visitor.
	"""
	session 		= models.CharField(max_length=64, **BLANK_NULL)
	ip_address 		= models.GenericIPAddressField(verbose_name="IP Address")
	widget 			= models.ForeignKey(Widget, on_delete=models.CASCADE)

	count 			= models.IntegerField(default=0)
	visitors 		= models.ManyToManyField("WidgetVisitor", blank=True)

	datetime		= models.DateTimeField(auto_now=True, verbose_name="Date")


	# ALTER SEQUENCE widgets_WidgetVisitor_id_seq RESTART WITH 1000;
	class Meta:
		verbose_name = "Widgets / Visitor"
		app_label = "lockers"


	def __str__(self):
		"""
		String value representative.
		"""
		return self.ip_address


	def clear():
		"""
		Delete old widget visitor rows.
		"""
		return __class__.objects.filter(
			datetime__lt=datetime.now() - timedelta(hour=1)
		).delete()



class WidgetEarnings(EarningsBase):
	"""
	Model for Widget's earnings.
	"""
	parent = models.OneToOneField(Widget, primary_key=True)


	class Meta:
		default_related_name = "earnings"