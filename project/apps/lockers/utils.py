from django.conf import settings
from ..lockers.lists.models import List
from ..lockers.files.models import File
from ..lockers.links.models import Link


def Locker(locker):
	try:
		locker = dict(settings.LOCKERS)[(locker).upper()]
		locker = eval(locker)

		return locker
	except:
		return None


def Locker_Item(locker, code):
	try:
		return Locker(locker).objects.get(code=code)
	except:
		return None


def Locker_Item_Reference(locker_obj):
	try:
		return (
			type(locker_obj).__name__,
			locker_obj.id,
			locker_obj.code
		)
	except:
		return (None, None, None,)
