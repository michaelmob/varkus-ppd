import django_tables2 as tables
from lockers.tables import LockerTableBase
from .models import Widget



class WidgetTable(LockerTableBase):
	"""
	Table that lists all of a user's widgets.
	"""
	name = tables.LinkColumn("widgets:detail", text=lambda r: r.name, args=(tables.A("code"),))

	class Meta(LockerTableBase.Meta):
		model = Widget
		empty_text = "You have not created any widgets."