from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from utils.constants import DEFAULT_BLANK_NULL

THREAD_PRIORITIES = (
	("1", "Low"),
	("2", "Normal"),
	("3", "High"),
	("4", "Urgent"),
	("5", "Emergency"),
)

THREAD_CATEGORIES = (
	("ACCOUNT", "Account"),
	("OFFERS", "Offers"),
	("LOCKERS", "Lockers"),
	("BILLING", "Billing"),
	("BUGS", "Bugs"),
	("OTHER", "Other"),
)

class Thread(models.Model):
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	category 	= models.CharField(max_length=16, choices=THREAD_CATEGORIES)
	priority 	= models.CharField(max_length=16, choices=THREAD_PRIORITIES, verbose_name="Priority")
	subject 	= models.CharField(max_length=100, verbose_name="Subject")
	closed 		= models.BooleanField(default=False)
	unread 		= models.BooleanField(default=True)
	datetime 	= models.DateTimeField(auto_now_add=True, verbose_name="Date")

	def __str__(self):
		return self.subject

	def get_absolute_url(self):
		return reverse("tickets-manage", args=(self.pk,))

	def posts(self):
		return Post.objects.filter(thread=self).order_by("-datetime")

	def last_post(self):
		return self.posts().last()


class Post(models.Model):
	thread 		= models.ForeignKey(Thread, on_delete=models.CASCADE)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE)
	message 	= models.TextField(max_length=1000, verbose_name="Message")
	file 		= models.FileField(upload_to="tickets/%Y/%m/%d/", **DEFAULT_BLANK_NULL)
	datetime 	= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message[:10]

from . import signals