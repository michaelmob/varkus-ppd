from datetime import datetime, timedelta
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from viking.utils.constants import DEFAULT_BLANK_NULL


# Categories for Thread
THREAD_CATEGORIES = (
	("ACCOUNT", "Account"),
	("OFFERS", "Offers"),
	("LOCKERS", "Lockers"),
	("BILLING", "Billing"),
	("BUGS", "Bugs"),
	("OTHER", "Other"),
)


# Priorities a Thread can have
THREAD_PRIORITIES = (
	("5", "Emergency"),
	("4", "Urgent"),
	("3", "High"),
	("2", "Normal"),
	("1", "Low"),
)



class Thread(models.Model):
	"""
	Model for Ticket Thread.
	"""
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	last_user 	= models.ForeignKey(User, related_name="last_user_id", null=True, on_delete=models.SET_NULL)
	category 	= models.CharField(max_length=16, choices=THREAD_CATEGORIES)
	priority 	= models.CharField(max_length=16, choices=THREAD_PRIORITIES, verbose_name="Priority")
	subject 	= models.CharField(max_length=100, verbose_name="Subject")
	last_replier = models.CharField(max_length=100, verbose_name="Last Replier")
	staff_unread = models.BooleanField(default=False)
	unread 		= models.BooleanField(default=False)
	closed 		= models.BooleanField(default=False, verbose_name="Status", help_text=(
		"Unchecked means the ticket is Open. Checked means the ticket is Closed."
	))
	ip_address	= models.GenericIPAddressField(verbose_name="IP Address")
	datetime 	= models.DateTimeField(auto_now_add=True, verbose_name="Date")


	def __str__(self):
		"""
		Ticket's string representation.
		"""
		return self.subject


	def get_absolute_url(self):
		"""
		Return URL for the Ticket's detail view.
		"""
		return reverse("tickets:detail", args=(self.pk,))


	def get_posts(self):
		"""
		Return posts belonging to Ticket Thread.
		"""
		return Post.objects.filter(thread=self).order_by("-datetime").prefetch_related("user")



class Post(models.Model):
	"""
	Model for Ticket Post.
	"""
	thread 		= models.ForeignKey(Thread, null=True)
	original	= models.BooleanField(default=False)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	message 	= models.TextField(max_length=5000, verbose_name="Message")
	file 		= models.FileField(upload_to="tickets/%Y/%m/", **DEFAULT_BLANK_NULL)
	ip_address	= models.GenericIPAddressField(verbose_name="IP Address")
	datetime 	= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		"""
		Post's string representation.
		"""
		return self.message[:10]


	def get_absolute_url(self):
		"""
		Return URL for the Ticket's detail view.
		"""
		try:
			return self.thread.get_absolute_url()
		except:
			""


	def can_delete(self):
		"""
		Returns if post is within deletion time of 1 day.
		"""
		return self.datetime > (datetime.now() - timedelta(days=1))