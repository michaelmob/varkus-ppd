from lockers.views.generic import LockerUnlockView



class ListUnlockView(LockerUnlockView):
	"""
	Custom Unlock view for List model.
	"""
	def access(self):
		"""
		Returns unlocked view. Sets token's 'data' field if not already set.
		"""
		if self.token.data:
			return

		# Get list item and set it as used
		item = self.object.get()
		item.used = True
		item.save()

		# Set token data to list item value
		self.token.data = item.value
		self.token.save()
