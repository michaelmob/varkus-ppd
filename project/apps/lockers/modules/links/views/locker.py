from lockers.views.generic import LockerUnlockView



class LinkUnlockView(LockerUnlockView):
	"""
	Custom Unlock view for Link model.
	"""
	def access(self):
		"""
		Returns unlocked view. When 'download' GET argument is present then
		return the download view.
		"""
		return super(__class__, self).access()