from django import template

register = template.Library()


@register.filter
def paginate(value, index):
	last_ = value[-1]
	from_ = index - 3
	to_ = index + 3

	if from_ < 1:
		from_ = 1

	if to_ > last_:
		to_ = last_

	return range(from_, to_ + 1)