from django.conf import settings

from ...bases.charts import View_Line_Chart_Base, View_Map_Chart_Base
from ...bases.manage import View_Overview_Base, View_Manage_Base, View_Delete_Base

from ..forms import Form_Create, Form_Edit
from ..models import List
from ..tables import Table_List


class View_Overview(View_Overview_Base):
	model 		= List
	form 		= Form_Create
	table 		= Table_List
	maximum 	= settings.MAX_LISTS
	template = "lists/manage/overview.html"


class View_Manage(View_Manage_Base):
	model 		= List
	form 		= Form_Edit
	template = "lists/manage/manage.html"


class View_Line_Chart(View_Line_Chart_Base):
	model 		= List


class View_Map_Chart(View_Map_Chart_Base):
	model 		= List


class View_Delete(View_Delete_Base):
	model 		= List