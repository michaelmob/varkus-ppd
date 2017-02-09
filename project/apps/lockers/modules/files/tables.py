from lockers.tables import LockerTableBase
from .models import File


class FileTable(LockerTableBase):
	"""
	Table that lists all of a user's files.
	"""

	class Meta(LockerTableBase.Meta):
		model = File
		empty_text = "You have not uploaded any files."