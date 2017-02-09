from django.conf import settings
from django.http import JsonResponse
from lockers.views import generic



class FileFormMixin(generic.ManageFormMixin):
	"""
	Modify .get_form_class() method to set placeholders for File's forms.
	"""
	placeholders = {
		"name": "My File",
		"description": "This is my file.",
	}



class FileCreateView(FileFormMixin, generic.ManageCreateView):
	"""
	Creation view to create and upload a file.
	"""
	fields = ["name", "description", "file"]


	def get_form_class(self):
		"""
		Add attributes to the file form field.
		"""
		form = super(__class__, self).get_form_class()
		attrs = form.base_fields["file"].widget.attrs
		attrs["style"] = "display:none"
		attrs["max-file-size"] = settings.MAX_UPLOAD_SIZE
		return form


	def get_form(self, *args, **kwargs):
		"""
		Extend .post() method to handle Ajax requests.
		"""
		form = super(__class__, self).get_form(*args, **kwargs)
		if self.request.FILES and self.request.FILES["file"].size > settings.MAX_UPLOAD_SIZE:
			form.add_error("file", "File size is too large.")
		return form


	def form_valid(self, form):
		"""
		If the form is valid, redirect to the supplied URL.
		"""
		response = super(__class__, self).form_valid(form)
		if self.request.is_ajax():
			return JsonResponse({
				"success": True,
				"data": {
					"url": self.get_success_url()
				}
			})
		return response


	def form_invalid(self, form):
		"""
		If the form is invalid, re-render the context data with the
		data-filled form and errors.
		"""
		if self.request.is_ajax():
			return JsonResponse(status=400, data={
				"success": False,
				"data": {
					"errors": form.errors.as_json()
				}
			})
		return self.render_to_response(self.get_context_data(form=form))
	


class FileUpdateView(FileFormMixin, generic.ManageUpdateView):
	"""
	Update view for editing files.
	"""
	fields = [
		# Details
		"name", "description"
	]
