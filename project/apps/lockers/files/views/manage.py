from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files import File as Django_File
from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render

from ...bases.charts import View_Line_Chart_Base, View_Map_Chart_Base
from ...bases.manage import View_Overview_Base, View_Manage_Base, View_Delete_Base

from ..models import File
from ..forms import Form_Edit
from ..tables import Table_File


class View_Overview(View_Overview_Base):
	model 		= File
	table 		= Table_File
	maximum 	= settings.MAX_FILES
	template 	= "files/manage/overview.html"


class View_Manage(View_Manage_Base):
	model 		= File
	form 		= Form_Edit
	template 	= "files/manage/manage.html"


class View_Line_Chart(View_Line_Chart_Base):
	model 		= File


class View_Map_Chart(View_Map_Chart_Base):
	model 		= File


class View_Delete(View_Delete_Base):
	model 		= File


class View_Upload(View):
	def get(self, request):
		return render(
			request, "files/manage/upload.html",
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