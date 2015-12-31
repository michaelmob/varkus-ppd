from django import template

register = template.Library()


@register.filter
def paginate(value, index):
	m = value[-1] + 1	# Max
	f = index - 3		# From
	t = index + 3 + 1	# To

	if f < 1:
		t += 1 - f
		f = 1

	if t > m:
		if f > 1:
			f -= 3 + 1 + (index - m)
		t = m

	return range(f, t)