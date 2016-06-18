from django.forms import ModelForm
from .models import Link, Earnings


class Form_Create(ModelForm):
	class Meta:
		model = Link
		fields = ["name", "url", "description"]

	def save(self, user):
		if not self.is_valid():
			return None

		return Link.create(
			user 		= user,
			name 		= self.cleaned_data["name"],
			description = self.cleaned_data["description"],
			url 		= self.cleaned_data["url"])


class Form_Edit(ModelForm):
	class Meta:
		model = Link
		fields = ["name", "description"]