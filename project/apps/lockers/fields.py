from django import forms
from django.conf import settings
from django.db import models
from django.forms.utils import flatatt
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError

import apps.lockers

LOCKERS_DICT = dict(settings.LOCKERS)


def locker_ref_to_object(value):
	try:
		# Assign to variables and check if model is valid
		model, id = value.split(",")[:2]
		LOCKERS_DICT[model.upper()]

		# Get class from model name and then retrieve object
		model = eval("apps.lockers.%ss.models.%s" % (model.lower(), model.title()))
		return model.objects.get(id=id)
	except:
		return None


class LockerInput(forms.Widget):
	def render(self, name, value, attrs=None):
		if value is None:
			value = ""
		
		# Defaults
		ref = ""
		ref_name = ""
		link = ""

		if value:
			ref = "%s,%s,%s" % (value.get_type().upper(), value.id, value.code)
			ref_name = " <strong>%s:</strong> %s" % (value.get_type().title(), value.code)
			link = " <a href='%s'>View</a>" % reverse("admin:lockers_%s_change" % value.get_type(), args=(value.id,))

		final_attrs = self.build_attrs(attrs, name=name)
		return format_html('<input{} value="{}"></input><br/>{}{}',
			flatatt(final_attrs), ref, mark_safe(ref_name), mark_safe(link))


class StorableLockerObject(object):
	def __init__(self, obj):
		self.locker = obj.__class__.__name__.upper()
		self.id = obj.id
		self.code = obj.code
		

class LockerField(models.Field):
	def __init__(self, *args, **kwargs):
		kwargs["max_length"] = 50
		kwargs["null"] = True
		kwargs["blank"] = True
		kwargs["default"] = None
		super(LockerField, self).__init__(*args, **kwargs)


	def get_internal_type(self):
		return "CharField"


	def formfield(self, **kwargs):
		kwargs.update({"widget": LockerInput})
		return super(LockerField, self).formfield(**kwargs)


	def storable(self, value):
		return StorableLockerObject(locker_ref_to_object(value))


	def pre_save(self, model_instance, add):
		""" Puts model instance into a storable locker object """
		value = super(LockerField, self).pre_save(model_instance, add)

		if not value:
			return None

		# Inputting as TEXT (LOCKER,ID,CODE)
		if isinstance(value, str):
			value = locker_ref_to_object(value)
			if not value:
				raise ValidationError("Locker object does not exist!")
				
		# Put the object into StorableLockerObject
		try:
			return StorableLockerObject(value)
		except AttributeError:
			raise ValueError("Invalid locker format! (Locker,ID,Code -> FILE,1,q98fk)")


	def get_prep_value(self, value):
		""" Converts storable locker object to comma seperated string """
		if not value:
			return None

		if not isinstance(value, StorableLockerObject):
			value = StorableLockerObject(value)

		return ",".join((value.locker, str(value.id), value.code))


	def from_db_value(self, value, expression, connection, context):
		""" Output of the value, so the model instance/locker object """
		if not value:
			return value

		return locker_ref_to_object(value)