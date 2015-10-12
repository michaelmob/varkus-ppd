from django.shortcuts import render

from ...bases.lockers import View_Locker, View_Unlock
from ..models import Link


class Locker(View_Locker):
	model = Link
	template = "lockers/links/locker.html"


class Unlock(View_Unlock):
	model = Link
	template = "lockers/links/unlock.html"

	def _return(self, request, obj):
		return render(
			request,
			self.template,
			{
				"obj": obj,
				"data": obj.url
			}
		)