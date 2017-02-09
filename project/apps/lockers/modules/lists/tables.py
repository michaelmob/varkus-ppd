from lockers.tables import LockerTableBase
from .models import List


class ListTable(LockerTableBase):
	"""
	Table that lists all of a user's lists.
	"""

	class Meta(LockerTableBase.Meta):
		model = List
		empty_text = "You have not created any lists."