from viking.utils import geoip
from viking.utils.user_agent import get_user_agent
from django.db.models import Q
from conversions.models import Conversion, Boost


class OfferDataContainer():
	"""
	Container for specific querying helpers and methods.
	"""
	def __init__(self, request, object_, count=30):
		"""
		Initialize Offer Container.
		"""
		# Defaults
		self.object_ids = []
		self.objects = []
		self.is_valid = True

		# Parameter values
		self.request = request
		self.object = object_
		self.count = count

		# User
		self.user = self.object.user
		self.profile = None
		if self.object and self.user and self.user.profile:
			self.profile = self.user.profile

		# Setup
		self.__set_identifiers()
		self.__set_args()


	def append(self, queryset):
		"""
		Append queryset of offers to `objects`.
		"""
		for object_ in queryset[:self.get_slots()]:
			if object_.id in self.object_ids:
				continue

			self.object_ids.append(object_.id)
			self.objects.append(object_)


	def result(self):
		"""
		Return results without duplicates.
		"""
		return self.objects


	def get_slots(self):
		"""
		Amount able to be accepted.
		"""
		return self.count - len(self.object_ids)


	def block_ids(self):
		"""
		User-blocked offers.
		"""
		if hasattr(self, "_block_ids"):
			return self._block_ids

		if self.profile:
			self._block_ids = self.profile.offer_block.values_list("id")
			return self._block_ids

		return []


	def priority_ids(self):
		"""
		User-prioritized offers.
		"""
		if hasattr(self, "_priority_ids"):
			return self._priority_ids

		if self.profile:
			self._priority_ids = self.profile.offer_priority.values_list("id")
			return self._priority_ids

		return []


	def boost_ids(self):
		"""
		User-boosted offers.
		"""
		if hasattr(self, "_boost_ids"):
			return self._boost_ids

		if self.user:
			self._boost_ids = (
				Boost.objects
					.filter(user=self.user, count__gt=0)
					.values_list("offer_id")
			)
			return self._boost_ids
		
		return []


	def exclude_ids(self):
		"""
		Exclude offers that user has aready completed.
		"""
		if hasattr(self, "_exclude_ids"):
			return self._exclude_ids

		self._exclude_ids = (
			Conversion.objects
				.filter(ip_address=self.ip_address)
				.values_list("offer_id")
		)
		return self._exclude_ids


	def __set_identifiers(self):
		"""
		Set class variables for user identifiers.
		"""
		self.ip_address = self.request.META.get("REMOTE_ADDR")
		self.country, self.city = geoip.get(self.ip_address)

		self.user_agent = self.request.META.get("HTTP_USER_AGENT")
		self.user_agent = get_user_agent(self.user_agent)

		if not self.country:
			self.is_valid = False

		if not self.city:
			self.city = "your area"


	def __set_args(self):
		"""
		Set class variables of filtering arguments.
		"""
		self.args = (
			Q(user_agent=self.user_agent) | Q(user_agent="") | Q(user_agent=None),
		)

		self.kwargs = {
			"countries__contains": self.country.upper(),
		} if self.country else {}

		if not (self.args and self.kwargs):
			self.is_valid = False