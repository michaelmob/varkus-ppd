from django.shortcuts import render

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Poll_Base, View_Redirect_Base
from ..models import List


class View_Locker(View_Locker_Base):
	model = List
	template = "lists/locker/locker.html"


class View_Redirect(View_Redirect_Base):
	model = List


class View_Unlock(View_Unlock_Base):
	model = List
	template = "lists/locker/unlock.html"

	def _return(self, request, obj):
		if not self.token.data:
			self.token.data = obj.get()
			self.token.save()

		return render(
			request,
			self.template,
			{
				"obj": obj,
				"data": self.token.data
			}
		)


class View_Poll(View_Poll_Base):
	model = List