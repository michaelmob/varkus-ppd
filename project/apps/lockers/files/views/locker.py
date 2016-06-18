from django.shortcuts import HttpResponse

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base
from ..models import File

from apps.conversions.models import Token


class View_Locker(View_Locker_Base):
	model = File
	template = "files/locker/locker.html"


class View_Redirect(View_Redirect_Base):
	model = File


class View_Unlock(View_Unlock_Base):
	model = File
	template = "files/locker/unlock.html"


class View_Download(View_Unlock_Base):
	model = File

	def access(self):
		try:
			if self.internal:
				return True
		except:
			pass

		return super(__class__, self).access()

	def get_return(self):
		response = HttpResponse(self._obj.file, content_type="application/octet-stream")
		response["Content-Disposition"] = "attachment; filename=\"%s\"" % \
			(self._obj.file_name).replace("\"", "").replace("\\", "")

		return response