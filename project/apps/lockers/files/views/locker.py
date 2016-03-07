from django.shortcuts import HttpResponse

from ...bases.lockers import View_Locker_Base, View_Unlock_Base, View_Redirect_Base, View_Poll_Base
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

	def access(self, request, obj):
		# if "locker__file_force" is set then return True
		# as we have internal permission to access the file
		try:
			if request.session["locker__file_force"]:
				del request.session["locker__file_force"]
				return True
		except KeyError:
			pass

		# Get token using request and the locker object
		try:
			self.token = Token.get(request, obj)
		except:
			return False

		# Return access
		return self.token.access()

	def get_return(self, request, obj):
		response = HttpResponse(obj.file, content_type="application/octet-stream")
		response["Content-Disposition"] = "attachment; filename=\"%s\"" % (obj.file_name).replace("\"", "").replace("\\", "")

		return response

class View_Poll(View_Poll_Base):
	model = File