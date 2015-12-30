from django.conf import settings

from ...bases.charts import View_Line_Chart_Base, View_Map_Chart_Base
from ...bases.manage import View_Overview_Base, View_Manage_Base, View_Delete_Base

from ..forms import Form_Create, Form_Edit
from ..models import Link
from ..tables import Table_Link


class View_Overview(View_Overview_Base):
	model 		= Link
	form 		= Form_Create
	table 		= Table_Link
	maximum 	= settings.MAX_LINKS
	template 	= "links/manage/overview.html"


class View_Manage(View_Manage_Base):
	model 		= Link
	form 		= Form_Edit
	template 	= "links/manage/manage.html"


class View_Line_Chart(View_Line_Chart_Base):
	model 		= Link


class View_Map_Chart(View_Map_Chart_Base):
	model 		= Link


class View_Delete(View_Delete_Base):
	model 		= Link