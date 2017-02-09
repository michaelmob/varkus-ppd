from django.conf import settings



class Deposit():
	"""
	Deposit class. 
	"""
	def __init__(self, *args):
		"""
		Construct Deposit class.
		"""
		self.user_id = args[0]
		self.company = args[1]
		self.affiliate_id = args[2]
		self.code = args[3]
		self.name = args[4]
		self.password = args[5]


	def search(column, value):
		"""
		Search `column` number for `value`.
		Return newly created Deposit object or first row's Deposit object.
		"""
		result = None

		for deposit in settings.DEPOSITS:
			if deposit[column] == value:
				result = deposit

		if not result:
			result = settings.DEPOSITS[0]
	
		return __class__(*result)


	def names():
		"""
		Return tuple of all deposit names.
		"""
		return ((d[3], d[4]) for d in settings.DEPOSITS)


	def default_affiliate_id():
		"""
		Return default affiliate ID.
		"""
		return settings.DEPOSITS[0][2]


	def default_password():
		"""
		Return default password.
		"""
		return settings.DEPOSITS[0][5]


	def get_by_user_id(user_id):
		"""
		Return deposit from a user ID.
		"""
		return __class__.search(0, user_id)


	def get_by_code(code):
		"""
		Return deposit from deposit's code.
		"""
		return __class__.search(3, code)


	def get_by_password(password):
		"""
		Return deposit from deposit's password.
		"""
		return __class__.search(5, password)