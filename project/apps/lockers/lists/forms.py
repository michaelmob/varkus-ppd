import json

from django.forms import ModelForm
from .models import List, Earnings


class Form_Create(ModelForm):
	class Meta:
		model = List
		fields = ["name", "description", "item_name", "items", "order", "delimeter", "reuse"]

	def create(self, user):
		obj = super(Form_Create, self).save(commit=False)

		# Set Delimeter to correct symbol
		delimeter = self.cleaned_data["delimeter"]
		if delimeter == "\\n":
			delimeter = "\n"

		elif delimeter == "space":
			delimeter = " "

		# Turn array into json string for database storage
		items = self.cleaned_data["items"]
		items = [[item, 0] for item in items.replace("\r", "").split(delimeter)]
		items_json = json.dumps(items, separators=(",", ":"))

		# Set Fields
		obj.user 		= user
		obj.code 		= List().generate_code()
		obj.description = self.cleaned_data["description"]
		obj.name 		= self.cleaned_data["name"]
		obj.item_name	= self.cleaned_data["item_name"]
		obj.items 		= items_json
		obj.item_count	= len(items)
		obj.order 		= self.cleaned_data["order"]
		obj.delimeter 	= self.cleaned_data["delimeter"]
		obj.reuse 		= self.cleaned_data["reuse"]
		obj.save()

		# Create Earnings
		Earnings.objects.get_or_create(obj=obj)

		return obj


class Form_Edit(ModelForm):
	class Meta:
		model = List
		fields = ["name", "description", "item_name", "order", "reuse"]
		#widget=forms.TextInput(attrs={"placeholder": "Examples: Item, Key, Code, Serial"})
