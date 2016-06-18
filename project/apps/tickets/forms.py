import re
from django import forms
from django.http import QueryDict
from django.forms import ModelForm
from .models import Thread, Post

class Form_Thread(ModelForm):
	message = forms.CharField(label="Message", widget=forms.Textarea)
	file = forms.FileField(label="File", required=False)

	class Meta:
		model = Thread
		fields = ("category", "priority", "subject", "message", "file")

	def __init__(self, request, **kwargs):
		self.request = request
		super(__class__, self).__init__(request.POST or None, **kwargs)

	def save(self):
		# Validate
		if not self.is_valid():
			return None

		# Create object
		obj = super(__class__, self).save(commit=False)

		# Set Thread Fields
		obj.user = self.request.user
		obj.save()

		# Create post
		Form_Post(self.request, obj).save()

		return obj


class Form_Post(ModelForm):
	class Meta:
		model = Post
		fields = ("message", "file")

	def __init__(self, request, thread, **kwargs):
		self.request = request
		self.thread = thread

		super(__class__, self).__init__(request.POST or None,
			request.FILES or None, **kwargs)

	def clean_message(self):
		return re.sub(r"(\r?\n){2,}", "\n\n", self.cleaned_data["message"])

	def save(self):
		# Validate
		if not self.is_valid():
			return None

		# Create object
		obj = super(__class__, self).save(commit=False)

		# Set Thread Fields
		obj.thread 	= self.thread
		obj.user 	= self.request.user
		obj.save()
		
		# Reset Form
		self.request.POST = QueryDict()
		
		return obj