from django.conf import settings
from django.core.exceptions import ValidationError


def validate_file(field):
	"""
	Validate file, be sure it is smaller than the maximum file size allowed.
	"""
	if field.file.size > settings.REPORT_MAX_FILE_SIZE:
		raise ValidationError("File size must be less than 4mb!")