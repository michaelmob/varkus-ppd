from django.conf import settings

from apps.lockers.lists.models 		import List
from apps.lockers.files.models 		import File
from apps.lockers.links.models 		import Link
from apps.lockers.widgets.models 	import Widget


def Locker(locker):
	try:
		locker = dict(settings.LOCKERS)[(locker).upper()]
		locker = eval(locker)

		return locker
	except:
		return None


def Locker_Object(locker, code, user=None):
	if not locker or not code:
		return None

	args = {"code": code}
	
	if user:
		args["user"] = user

	try:
		return Locker(locker).objects.get(**args)
	except:
		return None


def Locker_Object_Reference(locker_obj):
	try:
		return (
			type(locker_obj).__name__,
			locker_obj.id,
			locker_obj.code
		)
	except:
		return (None, None, None,)
