from django.conf import settings
import apps.lockers

LOCKERS_DICT = dict(settings.LOCKERS)

def locker_ref_to_object(value, code=False):
	try:
		# Assign to variables and check if model is valid
		model, val = value.split(",")[:2]
		LOCKERS_DICT[model.upper()]

		# Get class from model name and then retrieve object
		model = eval("apps.lockers.%ss.models.%s" % (model.lower(), model.title()))
		return model.objects.get(**{"code" if code else "id": val})
	except:
		return None