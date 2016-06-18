from django import template
from ..models import Announcement

register = template.Library()


@register.simple_tag
def broadcasts():
	return Announcement.broadcasts()