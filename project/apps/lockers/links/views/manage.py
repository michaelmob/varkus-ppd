from django.conf import settings

from ...bases.charts import View_Line_Chart, View_Map_Chart
from ...bases.manage import View_Overview, View_Manage, Delete_Base

from ..forms import Form_Create, Form_Edit
from ..models import Link
from ..tables import Table_Link


class Overview(View_Overview):
	template 	= "lockers/links/overview.html"
	model 		= Link
	form 		= Form_Create
	table 		= Table_Link
	maximum 	= settings.MAX_LINKS


class Manage(View_Manage):
	template 	= "lockers/links/manage/manage.html"
	model 		= Link
	form 		= Form_Edit


class Line_Chart(View_Line_Chart):
	model 		= Link


class Map_Chart(View_Map_Chart):
	model 		= Link


class Delete(Delete_Base):
	model 		= Link