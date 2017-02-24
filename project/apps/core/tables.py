import django_tables2 as tables
from django.utils.html import format_html
from django.utils.formats import date_format
from core.templatetags.currency import currency, cut_percent



class TableBase(tables.Table):
	"""
	Base Table class for all other tables to base themselves off of.
	"""
	template = "molds/table.html"

	class Meta:
		attrs = {
			"class": "ui sortable table",
			"th": {
				"_ordering": {
					"orderable": "sortable",
					"descending": "sorted descending",
					"ascending": "sorted ascending",
				}
			}
		}


	def currency(self, value, cut_amount=1):
		"""
		Format value into currency format.
		"""
		return "$%s" % currency(cut_percent(value, cut_amount))


	def date(self, value):
		"""
		Format date to the short format style.
		"""
		return date_format(value, "SHORT_DATE_FORMAT")


	def flag(self, value):
		"""
		Display flag.
		"""
		if not value:
			return format_html("<i class=\"world icon\"></i>")

		return format_html(
			"<i class=\"{} flag\" alt=\"{}\"></i>", value.lower(), value.upper()
		)



class CurrencyColumn(tables.Column):
	"""
	Currency column for django tables.
	"""
	def render(self, value):
		"""
		Formats currency column values in US currency format.
		"""
		return "$%s" % currency(value)