from django.conf import settings

from ...bases.charts import View_Line_Chart, View_Map_Chart
from ...bases.manage import View_Overview, View_Manage, Delete_Base

from ..models import Widget
from ..forms import Form_Create, Form_Edit
from ..tables import Table_Widget


class Overview(View_Overview):
	template 	= "lockers/widgets/display.html"
	model 		= Widget
	form 		= Form_Create
	table 		= Table_Widget
	maximum 	= settings.MAX_WIDGETS


class Manage(View_Manage):
	template 	= "lockers/widgets/manage/manage.html"
	model 		= Widget
	form 		= Form_Edit


class Line_Chart(View_Line_Chart):
	model 		= Widget


class Map_Chart(View_Map_Chart):
	model 		= Widget


class Delete(Delete_Base):
	model 		= Widget


def verify(user, code):
	""" Verify code and user owns object """
	if not code:
		return None

	obj = None

	try:
		obj = Widget.objects.get(user=user, code=code)
		return obj
	except Widget.DoesNotExist:
		return None