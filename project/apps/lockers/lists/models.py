import json
import random
from datetime import datetime
from ..models import models, Locker_Base, Earnings_Base

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

class List(Locker_Base):
	item_name		= models.CharField(max_length=100, verbose_name="Individual Item Name")
	item_count 		= models.IntegerField(default=0, verbose_name="Item Count")
	unlock_count	= models.IntegerField(default=0)
	order 			= models.CharField(max_length=20, default="descending", choices=ORDERS)
	delimeter 		= models.CharField(max_length=5, default="\\n", choices=DELIMETERS)
	reuse 			= models.BooleanField(default=False, verbose_name="Allow re-use of items")

	def create(user, name, item_name, description, items, delimeter, order, reuse):
		if delimeter == "\\n":
			delimeter = "\n"
			
		elif delimeter == "space":
			delimeter = " "

		items = items.replace("\r", "").split(delimeter)

		obj = List.objects.create(
			user 		= user,
			code 		= List().generate_code(),
			name 		= name,
			item_name 	= item_name,
			description = description,
			item_count	= len(items),
			order 		= order,
			delimeter 	= delimeter,
			reuse 		= True,
			datetime	= datetime.now()
		)

		Earnings.objects.get_or_create(obj=obj)
		List_Item.objects.bulk_create([List_Item(parent=obj, value=value) \
			for value in items])

		return obj

	def remaining(self):
		return self.item_count - self.unlock_count

	def reset(self):
		return List_Item.objects.filter(parent=self).update(used=False)

	def get(self):
		if self.order == "ASCENDING":
			return List_Item.objects.filter(parent=self, used=False).first()

		if self.order == "DESCENDING":
			return List_Item.objects.filter(parent=self, used=False).last()

		if self.order == "RANDOM":
			return List_Item.objects.filter(parent=self, used=False).order_by("?").first()


class Earnings(Earnings_Base):
	obj = models.OneToOneField(List, primary_key=True)
	
	class Meta:
		db_table = "lists_earnings"


class List_Item(models.Model):
	parent = models.ForeignKey(List, on_delete=models.CASCADE)
	value = models.CharField(max_length=1000)
	used = models.BooleanField(default=False)

	class Meta:
		verbose_name = "List Item"

	def __str__(self):
		return "[%s] %s" % (self.parent.name, self.value)