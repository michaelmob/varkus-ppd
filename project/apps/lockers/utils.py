from importlib import import_module
from django.conf.urls import url, include
from lockers.views import generic


def view_classes(model, view_type, view_class_names, **kwargs):
	"""
	Find model's view class objects from specified names.
	"""
	name = model.__name__.title()  # Titular model name
	modules = import_module("modules.%ss.views.%s" % (
		name.lower(), view_type.lower()
	))

	# Do not create dict if all we need is one class
	if type(view_class_names) is str:
		view_class_names = [view_class_names]
	else:
		views = {}

	# Loop through list of generic view types and set `view` (dict) elements
	# to those views if they can be found within the model's class otherwise
	# use default from generic manage/locker views
	for x in view_class_names:
		x_ = x.lower()

		# View exists
		if hasattr(modules, name + x + "View"):
			view = getattr(modules, name + x + "View")

		# View doesn't exist, so fetch the generic view
		else:
			view = getattr(generic, view_type.title() + x + "View")

		# Use the view as a view and set model of it
		view = view.as_view(model=model, **kwargs)

		if len(view_class_names) == 1:
			return view  # All we needed was one class, so return it

		views[x_] = view

	return views


def manage_url_patterns(model):
	"""
	Returns dynamically generated list of URL patterns for manage-based views.
	"""
	views = view_classes(model, "Manage", [
		"List", "Create", "Detail", "Update", "Delete", "ActivityChart"
	])
	
	# List of URL Patterns
	return [
		url(r"^$", views["list"], name="list"),
		url(r"^create/$", views["create"], name="create"),
		url(r"^(?P<slug>[A-z0-9]+)/", include([
			url(r"^$", views["detail"], name="detail"),
			url(r"^edit/$", views["update"], name="update"),
			url(r"^delete/$", views["delete"], name="delete"),
			url(r"^activity.json$", views["activitychart"], name="activity")
		]))
	]


def locker_url_patterns(model):
	"""
	Returns dynamically generated list of URL patterns for locker-based views.
	"""
	views = view_classes(model, "Locker", [
		"Lock", "Unlock", "Redirect"
	])
	
	# List of URL Patterns
	return [
		url(r"^(?P<slug>[A-z0-9]+)/", include([
			url(r"^$", views["lock"], name="lock"),
			url(r"^redirect/(?P<offer_id>[0-9]+)/$", views["redirect"], name="redirect"),
			url(r"^unlock/$", views["unlock"], name="unlock"),
			url(r"^unlock/(?P<action>[A-z]+)/$", views["unlock"], name="unlock-action"),
		]))
	]