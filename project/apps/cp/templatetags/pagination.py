from django import template

register = template.Library()


@register.simple_tag
def paginate(total, page, adjacent):
	# Total wanted to be shown in pagination
	wanted = (adjacent * 2) + 1

	# Less pages exist than the wanted amount; return the page count as is
	if total < wanted:
		return [ n for n in range(1, total + 1) ]

	# Create list of pages
	result = [ n for n in range(page - adjacent, page + adjacent + 1) \
		if n > 0 and n <= total ]

	# There are not enough items in the list
	if len(result) < wanted:
		# Calculate difference
		difference = wanted - len(result)

		# First page is 1
		if result[0] == 1:
			result += [ n + (result[-1] + 1) \
				for n in range(difference) ]

		# Last page is the last item
		elif result[-1] == total:
			result = [ n + (total - (adjacent * 2)) \
				for n in range(difference) ] + result

	return result