from django import forms
from django.forms import ModelForm
from .models import List, Earnings


class Form_Create(ModelForm):
	items = forms.CharField(widget=forms.Textarea)

	class Meta:
		model = List
		fields = ["name", "description", "item_name", "items", "order",
			"delimeter", "reuse"]

	def save(self, user):
		if not self.is_valid():
			return None

		return List.create(
			user 		= user,
			name 		= self.cleaned_data["name"],
			item_name	= self.cleaned_data["item_name"],
			description	= self.cleaned_data["description"],
			items 		= self.cleaned_data["items"],
			delimeter 	= self.cleaned_data["delimeter"],
			order 		= self.cleaned_data["order"],
			reuse 		= self.cleaned_data["reuse"])


class Form_Edit(ModelForm):
	class Meta:
		model = List
		fields = ["name", "description", "item_name", "order", "reuse"]
		#widget=forms.TextInput(attrs={"placeholder": "Examples: Item, Key, Code, Serial"})
