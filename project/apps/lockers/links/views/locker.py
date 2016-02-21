from django.shortcuts import render

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base, View_Poll_Base
from ..models import Link


class View_Locker(View_Locker_Base):
	model = Link
	template = "links/locker/locker.html"


class View_Redirect(View_Redirect_Base):
	model = Link


class View_Unlock(View_Unlock_Base):
	model = Link
	template = "links/locker/unlock.html"

	def get_return(self, request, obj):
		return render(
			request,
			self.template,
			{
				"obj": obj,
				"data": obj.url
			}
		)


class View_Poll(View_Poll_Base):
	model = Link