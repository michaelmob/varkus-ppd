from re import sub
from django import forms
from django.forms import ModelForm
from .models import Thread, Post



class ThreadForm(ModelForm):
	"""
	ModelForm for the ticket Thread model.
	"""
	message = forms.CharField(label="Message", widget=forms.Textarea)
	file = forms.FileField(label="File", required=False)


	class Meta:
		model = Thread
		fields = ("subject", "category", "priority", "message", "file")


	def save(self, commit=True):
		"""
		Creates opening post.
		"""
		self.instance = super(__class__, self).save(commit)

		if commit:
			post = PostForm(self.data, self.files).save(commit=False)
			post.original = True
			post.user = self.instance.user
			post.ip_address = self.ip_address
			post.thread = self.instance
			post.save()

		return self.instance



class PostForm(ModelForm):
	"""
	ModelForm for the ticket Post model.
	"""
	class Meta:
		model = Post
		fields = ("message", "file")


	def clean_message(self):
		"""
		Clean the message to not include too many whitespace or new lines.
		"""
		return sub(r"(\r?\n){2,}", "\n\n", self.cleaned_data["message"])


	def save(self, commit=True):
		"""
		Creates opening post.
		"""
		self.instance = super(__class__, self).save(commit)

		if commit:
			user = self.instance.user

			if user.is_staff:
				name = "%s %s." % (user.first_name, user.last_name[:1])
			else:
				name = user.username

			self.instance.thread.last_replier = name
			self.instance.thread.closed = False
			self.instance.thread.save()

		return self.instance