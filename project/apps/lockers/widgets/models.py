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

from ..models import Locker_Base, Earnings_Base
from utils.constants import DEFAULT_BLANK_NULL, BLANK_NULL
from utils.strings import random, WORDS

DEFAULTS = { "max_length": 300, "blank": True, "null": True }


class Widget(Locker_Base):
	locker_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, limit_choices_to={"app_label__in": ("lockers",)}, **BLANK_NULL)
	locker_id 	= models.PositiveIntegerField(**BLANK_NULL)
	locker 		= GenericForeignKey("locker_type", "locker_id")

	css_file 				= models.FileField(upload_to="widgets/css/", **DEFAULT_BLANK_NULL)
	http_notification_url 	= models.CharField(default=None, **DEFAULTS)
	standalone_redirect_url = models.CharField(default=settings.SITE_URL, **DEFAULTS)

	viral_mode 				= models.BooleanField(default=False)
	viral_visitor_count 	= models.IntegerField(default=5, verbose_name="Unique Visitors Required")
	viral_visitor_name		= models.CharField(default=None, verbose_name="Visitor Names (singular,plural)", **DEFAULTS)
	viral_message 			= models.CharField(default=None, verbose_name="Unsatisfied Amount Message", **DEFAULTS)

	def set_locker(self, obj):
		self.locker = obj or None
		self.save()

	def create(user, name, description):
		obj = Widget.objects.create(
			user 		= user,
			code 		= Widget().generate_code(),
			name 		= name,
			description	= description
		)
		Earnings.objects.get_or_create(obj=obj)
		return obj

	def read_css_file(self):
		buf = None
		if self.has_css_file():
			with open(self.css_file.path, "r") as f:
				buf = "".join(f.readlines())
		return buf

	def write_css_file(self, content):
		if self.has_css_file() or not content:
			self.css_file.delete()
		self.css_file.save(self.code + ".css", ContentFile(content), save=True)

	def visitor(self, request, pk=None):
		visitor, created = Widget_Visitor.objects.get_or_create(
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
			# Look for Widget_Visitor owner
			owner = Widget_Visitor.objects.filter(pk=pk).defer("widget").first()

			# Check if owner of widgets Widget_Visitor object exists and after
			# then check that the user isn't clicking on their own link, if that
			# passes then make sure the Widget_Visitor object is not already in the
			# owners visitors list
			if (
				owner and (request.META.get("REMOTE_ADDR") != owner.ip_address)
				and not owner.visitors.filter(
					session=request.session.session_key
				).exists()
			):
				# Add to 
				owner.visitors.add(visitor)
				owner.visitor_count = F("visitor_count") + 1
				owner.save()

				# Send channels message; we cant see if a new click was added
				# in a signal...
				Group("session-" + owner.session).send({
					"text": dumps({
						"success": True,
						"type": "CLICK",
						"message": self.viral_message_formatted(
							Widget_Visitor.objects.filter(pk=pk).only(
								"visitor_count"
							).first()
						)
					})
				})

		return (visitor, created)

	def viral_message_formatted(self, visitor):
		# Visitor names
		if not "," in self.viral_visitor_name:
			self.viral_visitor_name = "person,people"
		names = self.viral_visitor_name.split(",")

		# Amount left
		amount = self.viral_visitor_count - visitor.visitor_count
		name = escape(names[0] if amount < 2 else names[1])

		# User's message
		return (str(self.viral_message or settings.VIRAL_MESSAGE)
			.replace("{amount}", "<span id=\"amount\">%s</span>" % str(amount))
			.replace("{name}", name))


class Widget_Visitor(models.Model):
	session 		= models.CharField(max_length=64, **BLANK_NULL)
	ip_address 		= models.GenericIPAddressField(verbose_name="IP Address")
	widget 			= models.ForeignKey(Widget, on_delete=models.CASCADE)

	visitor_count 	= models.IntegerField(default=0)
	visitors 		= models.ManyToManyField("Widget_Visitor", blank=True)

	datetime		= models.DateTimeField(auto_now=True, verbose_name="Date")

	# ALTER SEQUENCE widgets_widget_visitor_id_seq RESTART WITH 1000;
	class Meta:
		verbose_name = "Visitor"

	def __str__(self):
		return self.ip_address

	def clear():
		return __class__.objects.filter(
			datetime__lt=datetime.now() - timedelta(hour=1)).delete()


class Earnings(Earnings_Base):
	obj = models.OneToOneField(Widget, primary_key=True)

	class Meta:
		db_table = "widgets_earnings"