from django import forms

CHOICES = (
	("2", "Prioritize this offer in my lockers",),
	("1", "Do not show this offer in my lockers",),
	("0", "I am neutral towards this offer",)
)


class OfferForm(forms.Form):
	priority = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

