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
			description = self.cleaned_data["description"]
		)


class Form_Edit(ModelForm):
	class Meta:
		model = Widget
		fields = ["name", "description"]


class Form_Viral(ModelForm):
	class Meta:
		model = Widget
		fields = [
			"viral_mode", "viral_visitor_count", "viral_visitor_name",
			"viral_message"
		]