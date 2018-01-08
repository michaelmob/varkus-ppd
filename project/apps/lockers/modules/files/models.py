import os
from hashlib import md5 as _md5
from django.db import models
from django.conf import settings
from lockers.models import LockerBase, EarningsBase



class File(LockerBase):
	"""
	Model for File locker.
	"""
	file 		= models.FileField(upload_to="files/%Y/%m/", default=None, blank=True, null=True)
	file_name 	= models.CharField(default="", max_length=300, blank=True, null=True)
	file_size 	= models.IntegerField()
	md5_sum		= models.CharField(max_length=32, blank=True, null=True)


	@classmethod
	def get_earnings_model(cls):
		"""
		Return earnings model for File.
		"""
		return FileEarnings


	def get_file_name(self):
		"""
		Return file's path and name or None if the file is non-existant.
		"""
		name = os.path.join(settings.MEDIA_ROOT, self.file.name)
		return name if os.path.exists(name) else None


	def save(self, *args, **kwargs):
		"""
		Extend .save() method to get set file's information from file.
		Returns the super class .save() method.
		"""
		# Object already exists
		if self.pk:
			return super(__class__, self).save(*args, **kwargs)

		# New Object
		md5 = _md5()
		for chunk in self.file.chunks():
			md5.update(chunk)
			self.md5sum = md5.hexdigest()

		# Set properties
		self.file_name = self.file.name
		self.file_size = self.file.size
		self.md5_sum = md5.hexdigest()

		return super(__class__, self).save(*args, **kwargs)



class FileEarnings(EarningsBase):
	"""
	Model for File's earnings.
	"""
	parent = models.OneToOneField(File, primary_key=True, on_delete=models.CASCADE)

	class Meta:
		default_related_name = "earnings"
