from lockers.tables import LockerTableBase
from .models import Link


class LinkTable(LockerTableBase):
	"""
	Table that lists all of a user's links
	"""

	class Meta(LockerTableBase.Meta):
		model = Link
		empty_text = "You have not created any links."