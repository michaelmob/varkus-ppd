from django import template
from django.utils.safestring import mark_safe
from django_countries import countries

register = template.Library()


""" Semantic UI Forms """
def generic_field(field, wrapper=None, **kwargs):
	"""
	Generic Field for Semantic UI inputs
		field -> formset field
		wrapper -> text surrounding, use %(widget)s for the field
		kwargs -> extra fields added to attributes
	"""
	# Default wrapper
	if not wrapper:
		wrapper = "<div class='ui input'>%(widget)s</div>" 

	# Start field tag
	html = "<div class='%sfield%s'>" % (
		"required " if (not "_noRequired" in kwargs) and field.field.required else "",
		" error" if (not "_noError" in kwargs) and field.errors else "" )

	# Label tag
	if (not "_noLabel" in kwargs) and field.label:
		html += "<label>%s</label>" % field.label

	# Remove private variables
	for key in ("_noLabel", "_noRequired", "_noError"):
		if key in kwargs:
			del kwargs[key]

	# Display widgets
	field.field.widget.attrs.update(kwargs)
	html += wrapper % {"widget": str(field)}

	# Errors
	for error in field.errors:
		html += "<div class='ui red pointing prompt label'>%s</div>" % error

	# End tag
	return mark_safe(html + "</div>")


@register.simple_tag()
def render_field(field, **kwargs):
	"""
	Render default field
		field -> formset field
	"""
	return generic_field(field, None, **kwargs)


@register.simple_tag()
def render_field_icon(field, icon, align="left", **kwargs):
	"""
	Render field with icon
		field -> formset field
		icon -> icon name (ex: "phone")
		align -> "left" or "right"
	"""
	# Top wrapper
	wrapper = "<div class='ui %s%sinput'>" % (
		align + " ",
		"icon " if icon else "" )

	# Widget
	wrapper += "%(widget)s"

	# Icon
	wrapper += "<i class='%s icon'></i></div>" % icon

	return mark_safe(generic_field(field, wrapper, **kwargs))


@register.simple_tag()
def render_field_dropdown(field, initial=None, **kwargs):
	"""
	Render dropdown menu
		field -> formset field
		initial -> initial value
	"""
	# Set initial value if set
	if not initial:
		field.initial = initial

	return mark_safe(generic_field(field, {"class": "ui dropdown"}, **kwargs))


@register.simple_tag()
def render_field_country(field, initial=None, placeholder="Select Country", **kwargs):
	"""
	Render dropdown box with country's flags and name (using django_countries)
		field -> country field
		initial -> initial value
		placeholder -> placeholder text for no value
	"""	
	# Set initial value if set
	if not initial:
		field.initial = initial

	# Put country code, lowercase country code for flag, and country name
	# into element and add them choices
	choices = ""

	for c in countries:
		x = (c[0], c[0].lower(), c[1]) # Code, Lowercase Code, Country Name
		choices += "<div class='item' data-value='%s'><i class='%s flag'></i>%s</div>" % x

	# Template
	wrapper = """
	<div class='ui fluid search selection dropdown'>
		<input name='%(name)s' type='hidden' value="%(initial)s">
		<i class='dropdown icon'></i>
		<div class='default text'>%(placeholder)s</div>
		<div class='menu'>
			%(choices)s
		</div>
	</div>
	""" % {
		"name": field.html_name, 
		"initial": initial,
		"placeholder": placeholder,
		"choices": choices
	}

	return mark_safe(generic_field(field, wrapper, **kwargs))


@register.simple_tag()
def render_field_checkbox(field, style="", **kwargs):
	"""
	Render checkbox field
		field -> formset field
		style -> style of checkbox (eg: toggle, slider)
	"""
	wrapper = "<div class='ui %s checkbox'>" % style
	wrapper += "%(widget)s"
	wrapper += "<label>%s</label></div>" % field.label

	kwargs.update({"_noLabel": True})

	return mark_safe(generic_field(field, wrapper, **kwargs))


@register.simple_tag()
def render_form(formset):
	"""
	Render all fields in formset
		formset -> django formset
	"""
	return mark_safe("".join([render_field(field) for field in formset]))