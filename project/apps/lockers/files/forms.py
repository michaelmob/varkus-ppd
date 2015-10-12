from django.forms import ModelForm
from .models import File

class Form_Edit(ModelForm):
	class Meta:
		model = File
		fields = ["name", "description"]