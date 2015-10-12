from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from utils import strings


class Thread(models.Model):
	PRIORITIES = (
		("1", "Low"),
		("2", "Normal"),
		("3", "High"),
		("4", "Urgent"),
	)

	TYPES = (
		("help", "Account Help"),
		("billing", "Billing"),
		("bug", "Bug Report"),
		("support", "Technical Support"),
		("other", "Other (Use if Unsure)"),
	)

	user = models.ForeignKey(User)
	ip_address = models.GenericIPAddressField()
	date_time = models.DateTimeField(auto_now_add=True, verbose_name="Date")
	priority = models.CharField(max_length=20, default="1", choices=PRIORITIES)
	type = models.CharField(max_length=50, default="other", choices=TYPES)
	subject = models.CharField(max_length=100, verbose_name="Subject")
	last_reply_user = models.ForeignKey(User, related_name="last_reply_user_id", verbose_name="Last Replier", default=None, blank=True, null=True)
	last_reply_date_time = models.DateTimeField(default=None, blank=True, null=True)
	closed = models.BooleanField(default=False, verbose_name="Status")
	staff_closed = models.BooleanField(default=False)
	unread = models.BooleanField(default=False)

	def __str__(self):
		return "%s: %s" % (self.pk, self.subject)

	def delete(self, *args, **kwargs):
		for post in Post.objects.filter(thread=self):
			post.image.delete()
		super(Thread, self).delete(*args, **kwargs)

	def save(self, *args, **kwargs):
		if self.staff_closed:
			self.closed = True
		super(Thread, self).save(*args, **kwargs)

	def create(user, ip_address, priority, type, subject, content, image=None):

		if Thread.objects.filter(user=user, subject=subject).count() > 1:
			return None

		thread = Thread.objects.create(
			user=user,
			ip_address=ip_address,
			date_time=datetime.now(),
			priority=priority,
			type=type,
			subject=subject
		)

		post = Post.create(
			thread=thread,
			thread_post=True,
			user=user,
			ip_address=ip_address,
			content=content,
			image=image,
		)

		return (thread, post)

	def type_human(self):
		# type from Key to Value: "help" -> "Account Help"
		return dict(self.TYPES)[self.type]

	def priority_human(self):
		# priority from Key to Value: "3" -> "High"
		return dict(self.PRIORITIES)[self.priority]

	def get(user):
		return Thread.objects.filter(user=user).order_by("-date_time")

	def admin_get():
		return Thread.objects.filter(staff_closed=False)\
			.order_by("-date_time")\
			.order_by("closed")\
			.order_by("-priority")\
			.order_by("-last_reply_date_time")

	def inverse(self, request, messages):
		# If thread was closed by staff we don't want the
		# user to re-open it
		if self.staff_closed:
			messages.error(request, "This ticket cannot be re-opened as it has been closed by a staff member.")
			return

		# Invert thread.closed
		self.closed = not self.closed

		# Check our inverted to see what we did
		if not self.closed:
			messages.success(request, "This ticket has been re-opened.")

		# Save the object
		self.save()

		# Return to our thread with the thread
		return

	def staff_close(self):
		self.closed = True
		self.staff_closed = True
		self.save()

		return self

	def exists(user, pk=None):
		if user.is_staff:
			try:
				thread = Thread.objects.get(pk=pk)
				return thread
			except:
				return None

		# If the entered pk is less than 1 then we know that
		# it's not a real ticket
		if int(pk) < 1:
			return None

		# Check if the ticket exists in the database
		# otherwise we'll return None so the thread view
		# will redirect to the list tickets view
		try:
			thread = Thread.objects.get(pk=pk, user=user)
			return thread
		except Thread.DoesNotExist:
			return None

	def posts(thread):
		return Post.objects.get(thread=thread)

	def is_unread(self):
		return self.unread and not self.closed and not self.staff_closed

	def unread_count(user):
		return Thread.objects.filter(user=user, unread=True, closed=False, staff_closed=False).count()


class Post(models.Model):
	thread = models.ForeignKey(Thread)
	thread_post = models.BooleanField(default=False)
	user = models.ForeignKey(User, default=None, blank=True, null=True)
	ip_address = models.GenericIPAddressField()
	date_time = models.DateTimeField(auto_now_add=True)
	content = models.TextField(max_length=1000)
	image = models.ImageField(upload_to="tickets/%Y/%m/", default=None, blank=True, null=True)

	def delete(self, *args, **kwargs):
		self.image.delete()
		super(Post, self).delete(*args, **kwargs)

	def create(user, thread, thread_post, ip_address, content, image):
		# No duplicates
		if Post.objects.filter(user=user, thread=thread, content=content).count() > 0:
			return None

		thread.unread = (not thread_post and thread.user != user)
		thread.last_reply_user = user
		thread.last_reply_date_time = datetime.now()
		thread.save()

		if thread.unread:
			thread_user = thread.user
			thread_user.profile.notification_ticket += 1
			thread_user.profile.save()

		post = Post.objects.create(
			thread=thread,
			thread_post=thread_post,
			user=user,
			ip_address=ip_address,
			date_time=datetime.now(),
			content=content,
		)

		if image:
			image = default_storage.save(
				# tickets/2014/11/15/19-(strlen32).jpg
				"tickets/%s/%s/%s" % (
					datetime.now().strftime("%Y/%m"),  # Year/Month
					thread.pk,  # Thread ID
					"%s-%s.%s" % (
						# 15-(strlen32).jpg
						post.pk,
						strings.random(32),
						image.name.split(".")[-1]
					)
				),
				image
			)

			post.image = image
			post.save()
		
		return post
		
	def __str__(self):
		return "%s: %s" % (self.pk, self.user)
