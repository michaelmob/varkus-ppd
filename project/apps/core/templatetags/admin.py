from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def modify_app_list(app_list):
	"""
	Modify the app list to merge 'users' models with 'auth' models.
	* This is purely an obsessive compulsive itch scratched. *
	"""
	auth_app = None
	users_app, users_app_index = None, None

	# Find user and auth app
	for idx, app in enumerate(app_list):
		if not users_app and app["app_label"] == "users":
			# Found users app
			users_app = app
			users_app_index = idx

		elif not auth_app and app["app_label"] == "auth":
			# Found auth app
			auth_app = app

		# Found both apps
		if auth_app and users_app:
			break

	# Add users models to auth models
	auth_app["models"] += users_app["models"]

	# Remove 'users' app from app_list
	del app_list[users_app_index]

	return ""