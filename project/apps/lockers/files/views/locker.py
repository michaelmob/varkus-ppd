from django.shortcuts import HttpResponse

from ...bases.lockers import View_Locker, View_Unlock
from ..models import File

from apps.leads.models import Token


class Locker(View_Locker):
	model = File
	template = "lockers/files/locker.html"


class Unlock(View_Unlock):
	model = File
	template = "lockers/files/unlock.html"


class Download(View_Unlock):
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
		self.token = Token.get(request, obj)

		# Return access
		return self.token.access()

	def _return(self, request, obj):
		response = HttpResponse(obj.file, content_type="application/octet-stream")
		response["Content-Disposition"] = "attachment; filename=\"%s\"" % (obj.file_name).replace("\"", "").replace("\\", "")

		return response