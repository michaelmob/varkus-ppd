from django import template

register = template.Library()


@register.simple_tag
def paginate(page, total_pages):
	"""
	Return pages in a paginated format.
	"""
	valid_pages = lambda s, e, t: (s if s > 1 else 1, e if e < t else t)

	adjacent = 2
	max_pages = (adjacent * 2) + 1

	# Start and end page numbers
	start = page - adjacent
	end = page + adjacent

	# Figure out valid pages
	start, end = valid_pages(start, end, total_pages)

	# Find difference and add extra pages
	diff = max_pages - (end - start) - 1
	if start == 1: end += diff
	elif end == total_pages: start -= diff

	# Disallow invalid pages
	start, end = valid_pages(start, end, total_pages)

	return range(start, end + 1)