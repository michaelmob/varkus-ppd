import json
import random
from datetime import datetime
from lockers.models import models, LockerBase, EarningsBase
from viking.utils.constants import BLANK_NULL

ORDERS = (
	("DESCENDING", "Descending"),
	("ASCENDING", "Ascending"),
	("RANDOM", "Random"),
)

DELIMETERS = (
	("\\n", "New Line (\\n)"),
	(",", "Comma (,)"),
	(";", "Semi-colon (;)"),
	("|", "Vertical bar (|)"),
	("-", "Dash (-)"),
	("space", "Space ( )"),
)



class List(LockerBase):
	"""
	Model for List locker.
	"""
	items			= models.TextField(max_length=11001, verbose_name="Items", **BLANK_NULL)
	item_name		= models.CharField(max_length=100, verbose_name="Individual Item Name")
	item_count 		= models.IntegerField(default=0, verbose_name="Item Count")
	unlock_count	= models.IntegerField(default=0)
	order 			= models.CharField(max_length=20, default="descending", choices=ORDERS)
	delimeter 		= models.CharField(max_length=5, default="\\n", choices=DELIMETERS)
	reuse 			= models.BooleanField(default=False, verbose_name="Allow re-use of items")


	@classmethod
	def get_earnings_model(cls):
		"""
		Return earnings model for File.
		"""
		return ListEarnings


	@property
	def remaining(self):
		"""
		Returns remaining item count.
		"""
		return self.item_count - self.unlock_count


	def save(self, *args, **kwargs):
		"""
		Extend .save() method to create list's items.
		Returns the super class .save() method.
		"""
		# Set delimeter to proper value
		if self.delimeter == "\\n":
			self.delimeter = "\n"
		elif self.delimeter == "space":
			self.delimeter = " "

		# Save object
		super(__class__, self).save(*args, **kwargs)
		if not self.items:
			return

		# Split the items
		items = self.items.replace("\r", "").split(self.delimeter)

		# Update fields
		self.items = None
		self.item_count = len(items)

		# Create list's items
		ListItem.objects.bulk_create([
			ListItem(parent=self, value=value) for value in items
		])


	def reset(self):
		"""
		Update List's items to unused.
		"""
		return ListItem.objects.filter(parent=self).update(used=False)


	def get(self):
		"""
		Return a ListItem depending on List's order field.
		"""
		# Filter arguments
		args = { "parent": self, "used": False }

		# Ascending order
		if self.order == "ASCENDING":
			return ListItem.objects.filter(**args).first()

		# Descending order
		if self.order == "DESCENDING":
			return ListItem.objects.filter(**args).last()

		# Random order
		if self.order == "RANDOM":
			return ListItem.objects.filter(**args).order_by("?").first()



class ListItem(models.Model):
	"""
	Model for a List's items.
	"""
	parent = models.ForeignKey(List, on_delete=models.CASCADE)
	value = models.CharField(max_length=100)
	used = models.BooleanField(default=False)


	class Meta:
		verbose_name = "List Item"


	def __str__(self):
		return "[%s] %s" % (self.parent.name, self.value)



class ListEarnings(EarningsBase):
	"""
	Model for List's earnings.
	"""
	parent = models.OneToOneField(List, primary_key=True)
	
	
	class Meta:
		default_related_name = "earnings"