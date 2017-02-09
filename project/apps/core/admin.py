from django.contrib.admin.options import InlineModelAdmin



class InlineInline(InlineModelAdmin):
	"""
	Inline inline.
	"""
	template = "admin/edit_inline/inline.html"