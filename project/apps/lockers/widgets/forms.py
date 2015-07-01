from django import forms


class Widget_Create(forms.Form):
	name = forms.CharField(max_length=100)

	description = forms.CharField(
		required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)



class Widget_Edit(forms.Form):
	name = forms.CharField(max_length=100)
	
	description = forms.CharField(
		required=False, max_length=500,
		widget=forms.Textarea(attrs={"style": "min-height:4rem;height:4rem"})
	)