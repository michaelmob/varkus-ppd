from django import template
from django_countries import countries

register = template.Library()


@register.inclusion_tag("_blueprint/data-block.html")
def data_block(color, value, title, icon, klass):
	return locals()


@register.inclusion_tag("_blueprint/data-block-two.html")
def data_block_two(color, value1, title1, value2, title2, icon, klass1, klass2):
	return locals()


@register.inclusion_tag("_blueprint/line.html")
def line_chart(dataUrl, title="Today's Activity"):
	return locals()


@register.inclusion_tag("_blueprint/map.html")
def map_chart(dataUrl, title="World Map"):
	return locals()


@register.inclusion_tag("_blueprint/table.html", takes_context=True)
def table(context, data, title, icon):
	return {"request": context["request"], "data": data, "title": title, "icon": icon}


@register.inclusion_tag("_blueprint/titlebar.html")
def titlebar(context, title, icon):
	return locals()


@register.simple_tag(takes_context=True)
def absolute(context, uri):
	return context["request"].build_absolute_uri("/")[:-1] + uri
