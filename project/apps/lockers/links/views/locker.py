from django.shortcuts import render

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base
from ..models import Link


class View_Locker(View_Locker_Base):
	model = Link
	template = "links/locker/locker.html"


class View_Redirect(View_Redirect_Base):
	model = Link


class View_Unlock(View_Unlock_Base):
	model = Link
	template = "links/locker/unlock.html"

	def data(self):
		return self._obj.url