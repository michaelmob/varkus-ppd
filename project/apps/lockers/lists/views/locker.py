from django.shortcuts import render

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base
from ..models import List


class View_Locker(View_Locker_Base):
	model = List
	template = "lists/locker/locker.html"


class View_Redirect(View_Redirect_Base):
	model = List


class View_Unlock(View_Unlock_Base):
	model = List
	template = "lists/locker/unlock.html"

	def get_return(self):
		if not self.token.data:
			# Get list item and set it as used
			obj = self._obj.get()
			obj.used = True
			obj.save()

			# Set token data to list item value
			self.token.data = obj.value
			self.token.save()

		return super(View_Unlock, self).get_return()