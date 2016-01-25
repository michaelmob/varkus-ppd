from django.forms import ModelForm
from .models import Widget, Earnings


class Form_Create(ModelForm):
	class Meta:
		model = Widget
		fields = ["name", "description"]

	def create(self, user):
		obj = super(Form_Create, self).save(commit=False)
		
		# Set Fields
		obj.user = user
		obj.code = Widget().generate_code()
		obj.name = self.cleaned_data["name"]
		obj.description = self.cleaned_data["description"]
		obj.save()

		# Create Earnings
		Earnings.objects.get_or_create(obj=obj)

		return obj


class Form_Edit(ModelForm):
	class Meta:
		model = Widget
		fields = ["name", "description"]