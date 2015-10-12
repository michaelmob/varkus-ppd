from django.conf import settings

from ...bases.charts import View_Line_Chart, View_Map_Chart
from ...bases.manage import View_Overview, View_Manage, Delete_Base

from ..forms import Form_Create, Form_Edit
from ..models import List
from ..tables import Table_List


class Overview(View_Overview):
	template 	= "lockers/lists/overview.html"
	model 		= List
	form 		= Form_Create
	table 		= Table_List
	maximum 	= settings.MAX_LISTS


class Manage(View_Manage):
	template 	= "lockers/lists/manage/manage.html"
	model 		= List
	form 		= Form_Edit


class Line_Chart(View_Line_Chart):
	model 		= List


class Map_Chart(View_Map_Chart):
	model 		= List


class Delete(Delete_Base):
	model 		= List