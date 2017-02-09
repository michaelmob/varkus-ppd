import os
from django.test.runner import DiscoverRunner
from django.conf import settings



class TestRunner(DiscoverRunner):
	"""
	Test runner to only run tests from `INSTALLED_APPS`.
	"""
	def get_apps(self, dir, prefix=""):
		"""
		Get app names within a directory.
		"""
		cwd = os.getcwd()
		return [
			prefix + name for name in os.listdir(dir)
				if not name.startswith("_") and
				os.path.isdir(os.path.join(cwd, dir, name))
		]


	def run_tests(self, test_labels, *args, **kwargs):
		"""
		Run tests that belong to our app directories.
		"""
		if not test_labels:
			apps = self.get_apps("apps")
			#modules = self.get_apps("apps/lockers/modules", "modules.")
			test_labels = apps# + modules

		return super(__class__, self).run_tests(
			test_labels, *args, **kwargs
		)