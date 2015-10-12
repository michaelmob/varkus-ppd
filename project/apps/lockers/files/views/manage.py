from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files import File as Django_File
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render

from ...bases.charts import View_Line_Chart, View_Map_Chart
from ...bases.manage import View_Overview, View_Manage, Delete_Base

from ..models import File
from ..forms import Form_Edit
from ..tables import Table_File


class Overview(View_Overview):
	template 	= "lockers/files/overview.html"
	table 		= Table_File
	maximum 	= settings.MAX_FILES


class Manage(View_Manage):
	template 	= "lockers/files/manage/manage.html"
	model 		= File
	form 		= Form_Edit


class Line_Chart(View_Line_Chart):
	model 		= File


class Map_Chart(View_Map_Chart):
	model 		= File


class Delete(Delete_Base):
	model 		= File


class Upload(View):
	def get(self, request):
		return render(
			request, "lockers/files/upload.html",
			{"MAX_UPLOAD_SIZE": settings.MAX_UPLOAD_SIZE}
		)

	def post(self, request):
		success = False
		value = ""
		errors = 0

		count = File.objects.filter(user=request.user).count()

		if(count >= settings.MAX_FILES):
			return JsonResponse({
				"success": False,
				"value": "You have reached your maximum file limit."
			})

		disallowed_exts = [
			"exe", "bat", "com", "cmd", "vbs", "vbscript", "py",
		]

		# File Exists
		try:
			_file = Django_File(request.FILES["file"])
		except:
			value = "No file was delivered"
			errors += 1

		# File Type
		if errors < 1:
			ext = str(_file.name).lower().split('.')[-1]

			if(ext in disallowed_exts):
				value = "Disallowed file type"
				errors += 1

		# File Size
		if errors < 1:
			if(_file.size > settings.MAX_UPLOAD_SIZE):
				value = "File too large"
				errors += 1

		# Create File
		if errors < 1:
			obj = File.create(
				user=request.user,
				file=_file
			)

			success = True
			value = reverse("files-manage", args=[obj.code])

		return JsonResponse({
			"success": success,
			"value": value
		})