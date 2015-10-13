from django.shortcuts import render

from ...bases.lockers import View_Locker, View_Unlock, View_Poll
from ..models import List


class Locker(View_Locker):
	model = List
	template = "lockers/lists/locker.html"


class Unlock(View_Unlock):
	model = List
	template = "lockers/lists/unlock.html"

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

class Poll(View_Poll):
	model = List