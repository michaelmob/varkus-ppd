from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from datetime import datetime, timedelta

from .forms import Form_Ticket_Create, Form_Ticket_Post
from .models import Thread, Post

from utils import dicts, files, paginate


@staff_member_required
def staff_list(request, page=1):
	threads = paginate.pages(Thread.admin_get(), 15, page)
	
	return render(
		request, "tickets/staff.html",
		{
			"threads": threads
		}
	)


def list(request, page=1):
	threads = paginate.pages(Thread.get(request.user), 15, page)

	if request.user.profile.notification_ticket > 0:
		request.user.profile.notification_ticket = 0
		request.user.profile.save()

	if request.POST:
		form = Form_Ticket_Create(request.POST)
		errors = 0

		if form.is_valid():
			image = request.FILES.get("image", None)

			if image:
				if len(image) > settings.REPORT_MAX_FILE_SIZE:
					messages.error(request, "Files may not be larger than 4 megabytes.")
					errors += 1

				if not files.check_image(image):
					messages.error(request, "Uploaded files must be images.")
					errors += 1

			if errors < 1:
				thread = Thread.create(
					request.user,
					request.META.get("REMOTE_ADDR"),
					form.cleaned_data["priority"],
					form.cleaned_data["type"],
					form.cleaned_data["subject"],
					form.cleaned_data["message"],
					image
				)

				if thread:
					messages.success(request, "Your ticket has been created!")
					return redirect("tickets-thread", thread[0].pk)
				else:
					messages.error(
						request,
						"Your ticket has not been created " +
						"because it is a duplicate."
					)
	else:
		form = Form_Ticket_Create()

	return render(
		request, "tickets/list.html",
		{
			"threads": threads,
			"form": form,
			"types": Thread.TYPES,
			"priorities": Thread.PRIORITIES
		}
	)


def thread(request, id=None, action=None):
	# Get our ticket, if it doesn't exist
	# redirect them back to the ticket list
	thread = Thread.exists(request.user, id)

	if not thread:
		return redirect("tickets")

	form = Form_Ticket_Post(request.POST if request.POST else None)

	# Create our form
	if action:
		action = action.lower()

		if request.POST and action == "set":
			thread.inverse(request, messages)

		elif form.is_valid() and action == "post":
			image = request.FILES.get("image", None)

			# Format Image
			errors = 0
			if image:
				# Set Image to the uploaded image

				if len(image) > settings.REPORT_MAX_FILE_SIZE:
					messages.error(request, "Files may not be larger than 4 megabytes.")
					errors += 1

				if not files.check_image(image):
					messages.error(request, "Uploaded files must be images.")
					errors += 1

			message = request.POST.get("message")

			if (errors > 0):
				pass
			elif not(thread.staff_closed or thread.closed):
				# Create post
				if Post.create(
					user=request.user,
					thread=thread,
					thread_post=False,
					ip_address=request.META.get("REMOTE_ADDR"),
					content=message,
					image=image
				):
					messages.success(request, "Your message has been posted.")
				else:
					messages.error(request, "Your message has not been posted because it is a duplicate.")

				form = Form_Ticket_Post()
			else:
				messages.error(request, "You cannot post a message to this closed ticket.")

		elif action == "delete":
			id = request.GET.get("id", None)
			if id:
				try:
					post = Post.objects.get(user=request.user, id=id)

					if post.date_time > datetime.now() + timedelta(hours=2):
						messages.error(request, "You cannot delete your message two hours after it has been posted.")
					elif post.thread_post:
						messages.error(request, "You cannot delete the opening message.")
					else:
						post.delete()
						messages.success(request, "Your message has been deleted.")
				except:
					pass

	# Let the her know what's with her ticket
	if thread.staff_closed:
		messages.error(request, "This ticket is currently closed. You may not re-open it. Should a new issue arise, you may create a new ticket.")

	elif thread.closed:
		messages.error(request, "This ticket is currently closed. You may re-open it.")

	# Get Messages
	posts = Post.objects.filter(thread=thread).order_by("date_time")

	return render(
		request, "tickets/thread.html",
		{
			"thread": thread,
			"posts": posts,
			"form": form
		}
	)
