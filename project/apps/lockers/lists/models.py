import json
import random
from datetime import datetime
from django.db import models
from ..models import Locker_Base, Earnings_Base


class List(Locker_Base):

	ORDERS = (
		("descending", "Descending"),
		("ascending", "Ascending"),
		("random", "Random"),
	)

	DELIMETERS = (
		("\\n", "New Line (\\n)"),
		(",", "Comma (,)"),
		(";", "Semi-colon (;)"),
		("|", "Vertical bar (|)"),
		("-", "Dash (-)"),
		("space", "Space ( )"),
	)

	item_name		= models.CharField(max_length=100)
	items 			= models.TextField(max_length=6000)
	item_count 		= models.IntegerField()
	unlock_count	= models.IntegerField(default=0)
	order 			= models.CharField(max_length=20, default="descending", choices=ORDERS)
	delimeter 		= models.CharField(max_length=5, default="\\n", choices=DELIMETERS)
	reuse 			= models.BooleanField(default=False)

	def __str__(self):
		return "%s: %s" % (self.pk, self.name)

	def create(user, name, item_name, description, items, delimeter, order, reuse):
		if delimeter == "\\n":
			delimeter = "\n"
		elif delimeter == "space":
			delimeter = " "

		items = [[item, 0] for item in items.replace("\r", "").split(delimeter)]
		items_json = json.dumps(items, separators=(",", ":"))

		obj = List.objects.create(
			user 		= user,
			code 		= List().generate_code(),
			name 		= name,
			item_name 	= item_name,
			description = description,
			items 		= items_json,
			item_count	= len(items),
			order 		= order,
			delimeter 	= delimeter,
			reuse 		= True,
			date_time	= datetime.now()
		)

		Earnings.objects.get_or_create(obj=obj)

		return obj

	def remaining(self):
		return self.item_count - self.unlock_count

	def items_list(self):
		return json.loads(self.items)

	def reset(self, descending=True):
		items = [[item[0], 0] for item in json.loads(self.items)]

		if not descending:
			items = items[::-1]

		self.items = json.dumps(items, separators=(",", ":"))
		self.unlock_count = 0
		self.save()
		return items

	def get(self):
		if self.order == "descending":
			return self.get_order(True)
		elif self.order == "ascending":
			return self.get_order(False)
		elif self.order == "random":
			return self.random()

	def get_order(self, descending=True):
		# Grab our items list, list of lists
		# first [0] is the content, second [1] is use
		# ([1] == 0) == Not used
		# ([1] == 1) == Already used
		items = self.items_list()

		# Reverse array if not descending
		if not descending:
			items = items[::-1]

		# Check last item, to see if list is finished
		if items[-1][1] == 1:
			if self.reuse:
				# List can be re-used so reset items
				items = self.reset(descending)
			else:
				# Return none since we aren't re-using the list
				return None

		# Loop through items to see if they have been given out
		for i, item in enumerate(items):
			if item[1] == 0:
				# Set use to 1 to signify it's been used, and then encode
				# to json and save the object
				items[i][1] = 1
				
				if not descending:
					items = items[::-1]
				
				self.items = json.dumps(items, separators=(",", ":"))
				self.unlock_count += 1
				self.save()

				# Return the content
				return item[0]

	def random(self):
		items = self.items_list()
		unused = []

		for item in items:
			if item[1] == 0:
				unused.append(item)

		if len(unused) < 1:
			if self.reuse:
				self.reset()
				return self.random()
			else:
				return None

		random_item = random.choice(unused)

		items[items.index(random_item)][1] = 1
		
		self.items = json.dumps(items, separators=(",", ":"))
		self.unlock_count += 1
		self.save()

		return random_item[0]


class Earnings(Earnings_Base):
	obj 		= models.OneToOneField(List, primary_key=True)

	class Meta:
		verbose_name = "Earnings"
		verbose_name_plural = "Earnings"
