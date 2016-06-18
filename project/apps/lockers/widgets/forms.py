from django.forms import ModelForm
from .models import Widget, Earnings


class Form_Create(ModelForm):
	class Meta:
		model = Widget
		fields = ["name", "description"]

	def save(self, user):
		if not self.is_valid():
			return None
		
		return Widget.create(
			user 		= user,
			name 		= self.cleaned_data["name"],
			description = self.cleaned_data["description"])


class Form_Edit(ModelForm):
	class Meta:
		model = Widget
		fields = ["name", "description"]