from django.http import FileResponse
from lockers.views.generic import LockerUnlockView



class FileUnlockView(LockerUnlockView):
	"""
	Custom Unlock view for File model.
	"""
	def access(self):
		"""
		Returns unlocked view. When 'download' GET argument is present then
		return the download view.
		"""
		if self.request.GET.get("download"):
			response = self.download()
			if response:
				return response


	def download(self):
		"""
		Returns download view if File exists, otherwise returns None and the
		unlock page is shown again.
		"""
		name = self.object.get_file_name()
		if not name:
			return

		response = FileResponse(open(name, "rb"))
		response["Content-Disposition"] = (
			"attachment; filename=\"%s\"" % (
				self.object.file_name.replace("\"", "").replace("\\", "")
			)
		)
		return response