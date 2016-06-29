from django.conf import settings

from ...bases.charts import View_Line_Chart_Base, View_Map_Chart_Base
from ...bases.manage import View_Overview_Base, View_Manage_Base, View_Delete_Base

from ..models import Widget
from ..forms import Form_Create, Form_Edit
from ..tables import Table_Widget


class View_Overview(View_Overview_Base):
	model 		= Widget
	form 		= Form_Create
	table 		= Table_Widget
	maximum 	= settings.MAX_WIDGETS
	template 	= "widgets/manage/overview.html"


class View_Manage(View_Manage_Base):
	model 		= Widget
	form 		= Form_Edit
	template 	= "widgets/manage/manage.html"


class View_Line_Chart(View_Line_Chart_Base):
	model 		= Widget


class View_Map_Chart(View_Map_Chart_Base):
	model 		= Widget


class View_Delete(View_Delete_Base):
	model 		= Widget