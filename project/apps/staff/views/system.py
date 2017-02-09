import sys, platform, psutil
from django.views.generic import TemplateView
from braces import views as braces



class SystemView(braces.LoginRequiredMixin, braces.SuperuserRequiredMixin, TemplateView):
	"""
	Superuser view to show the superuser all the system details.
	"""
	template_name = "staff/system_detail.html"


	def get_context_data(self):
		"""
		Extend context dictionary to include specifications and details.
		"""
		context = super(__class__, self).get_context_data()

		ram = psutil.virtual_memory()
		swap = psutil.swap_memory()
		disk = psutil.disk_usage("/")

		context.update({
			# Monitor
			"cpu": psutil.cpu_percent(interval=1),
			"ram": [ram.used, ram.total],
			"swap": [swap.used, swap.total],
			"disk": [disk.used, disk.total],

			# Specfications
			"system": platform.system(),
			"release": platform.release(),
			"version": platform.version(),
			"machine": platform.machine(),
			"python": sys.version
		})

		return context