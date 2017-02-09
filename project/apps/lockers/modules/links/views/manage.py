from django.conf import settings
from lockers.views import generic



class LinkFormMixin(generic.ManageFormMixin):
	"""
	Modify .get_form_class() method to set placeholders for Link's forms.
	"""
	placeholders = {
		"name": "My Link",
		"description": "This is my link.",
		"url": settings.SITE_URL
	}

	

class LinkCreateView(LinkFormMixin, generic.ManageCreateView):
	"""
	Creation view to create a link.
	"""
	fields = ["name", "url", "description"]
	


class LinkUpdateView(LinkFormMixin, generic.ManageUpdateView):
	"""
	Update view for editing links.
	"""
	fields = ["name", "url", "description"]
