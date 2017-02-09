from lockers.views import generic



class ListFormMixin(generic.ManageFormMixin):
	"""
	Modify .get_form_class() method to set placeholders for List's forms.
	"""
	placeholders = {
		"name": "My List",
		"description": "This is my list.",
		"items": "Item 1\nItem 2\nItem 3",
		"item_name": "Item"
	}

	

class ListCreateView(ListFormMixin, generic.ManageCreateView):
	"""
	Creation view to create a list.
	"""
	fields = [
		"name", "items", "item_name", "order", "delimeter", "reuse", 
		"description"
	]


	def get_form_class(self):
		"""
		Modify form to set 'items' field to required.
		"""
		form = super(__class__, self).get_form_class()
		form.base_fields["items"].required = True
		form.base_fields["order"].initial = ""
		return form
	


class ListUpdateView(ListFormMixin, generic.ManageUpdateView):
	"""
	Update view for editing lists.
	"""
	fields = ["name", "description", "item_name", "order", "reuse"]
