from django.conf import settings

def is_postgres():
	return settings.DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql_psycopg2"

# Does the same thing as distinct does
def distinct_column(queryset, column):
	pks = queryset.values_list("pk", column).distinct()
	column_pks = []
	new_pks = []

	# For every key, check that the column's ID is not in the list of columns
	# and if it isn't then append it to the list, so we know not to add it
	# to the new set of keys
	for pk in pks:
		if pk[1] not in column_pks:
			column_pks.append(pk[1])
			new_pks.append(pk[0])

	# Re-fetch new queryset but with only one of the column, just as distinct
	# would do... had I been using postgresql
	return queryset.model.objects.filter(pk__in=new_pks)