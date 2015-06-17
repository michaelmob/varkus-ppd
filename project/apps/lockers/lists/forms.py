from django import forms
from .models import List


class List_Create(forms.Form):
	name = forms.CharField(max_length=100)

	description = forms.CharField(
		required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)

	item_name = forms.CharField(
		max_length=20,
		widget=forms.TextInput(attrs={"placeholder": "Examples: Item, Key, Code, Serial"})
	)

	items = forms.CharField(max_length=5000, widget=forms.Textarea)
	order = forms.ChoiceField(choices=List.ORDERS)
	delimeter = forms.ChoiceField(choices=List.DELIMETERS)
	reuse = forms.BooleanField(required=False)


class List_Edit(forms.Form):
	name = forms.CharField(max_length=100)
	
	description = forms.CharField(
		required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)

	item_name = forms.CharField(
		max_length=20,
		widget=forms.TextInput(attrs={"placeholder": "Examples: Item, Key, Code, Serial"})
	)

	order = forms.ChoiceField(choices=List.ORDERS)
	reuse = forms.BooleanField(required=False)
