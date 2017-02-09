from django import template
from django.utils.html import format_html
from django_countries import countries

register = template.Library()


@register.simple_tag
def data_block_content(value, title, klass=""):
	"""
	Data block content is a value, a title, and a class name.
	"""
	return locals()


@register.inclusion_tag("molds/data_block.html")
def data_block(color, icon, content):
	"""
	Colored data block with a value and title.
	"""
	return {
		"color": color,
		"icon": icon,

		"value": content["value"],
		"title": content["title"],
		"klass": content["klass"]
	}


@register.inclusion_tag("molds/data_block_duo.html")
def data_block_duo(color, icon, content_1, content_2):
	"""
	Colored data block with two values and titles.
	"""
	return {
		"color": color,
		"icon": icon,

		"value1": content_1["value"],
		"title1": content_1["title"],
		"klass1": content_1["klass"],

		"value2": content_2["value"],
		"title2": content_2["title"],
		"klass2": content_2["klass"]
	}


@register.simple_tag
def render_titlebar(title, icon="square"):
	"""
	Returns HTML titlebar for containers.
	"""
	return format_html((
		"<div class=\"ui top attached inverted red menu\">"
		"<div class=\"icon header item\"><i class=\"{} icon\"></i></div>"
		"<div class=\"header item\">{}</div>"
		"</div>"
	), icon, title)


@register.inclusion_tag("molds/activity_chart.html")
def render_activity_chart():
	"""
	Returns activity/line chart HTML file to be included.
	"""
	return locals()


@register.inclusion_tag("molds/map_chart.html")
def render_map_chart():
	"""
	Returns map chart HTML file to be included.
	"""
	return locals()


@register.inclusion_tag("molds/table.html", takes_context=True)
def render_table(context, data):
	"""
	Returns table HTML file to be included.
	"""
	return {"request": context["request"], "data": data}


@register.simple_tag(takes_context=True)
def absolute_url(context, uri):
	"""
	Returns absolute URL for site.
	"""
	return context["request"].build_absolute_uri("/")[:-1] + uri