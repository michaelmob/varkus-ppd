from django.forms import ModelForm
from .models import Link, Earnings


class Form_Create(ModelForm):
	class Meta:
		model = Link
		fields = ["name", "url", "description"]

	def create(self, user):
		obj = super(Form_Create, self).save(commit=False)
		
		# Set Fields
		obj.user = user
		obj.code = Link().generate_code()
		obj.name = self.cleaned_data["name"]
		obj.description = self.cleaned_data["description"]
		obj.url = self.cleaned_data["url"]
		obj.save()

		# Create Earnings
		Earnings.objects.get_or_create(obj=obj)

		return obj


class Form_Edit(ModelForm):
	class Meta:
		model = Link
		fields = ["name", "description"]