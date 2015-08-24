from django import forms
from .models import Thread


class Form_Ticket_Create(forms.Form):
	subject = forms.CharField(max_length=100)
	type = forms.ChoiceField(choices=Thread.TYPES)
	priority = forms.ChoiceField(choices=Thread.PRIORITIES)
	message = forms.CharField(min_length=20, max_length=1000,
		widget=forms.Textarea(attrs={"rows": 3}))
	image = forms.ImageField(required=False)


class Form_Ticket_Post(forms.Form):
	message = forms.CharField(min_length=20, max_length=1000,
		widget=forms.Textarea(attrs={"rows": 3}))
	image = forms.ImageField(required=False)
