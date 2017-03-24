from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.html import escape

register = template.Library()


@register.simple_tag(takes_context=True)
def code(context, language, filename, **kwargs):
	"""
	Render template as code by replacing less than and greater signs with
	HTML entities.
	"""
	kwargs["request"] = context["request"]
	return mark_safe(
		"<pre class=\"language-%s\"><code>%s</code></pre>" % (
			language, escape(render_to_string(filename, kwargs)).strip()
		)
	)