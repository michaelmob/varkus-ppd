from datetime import date, timedelta
from django import forms


CALENDAR_ATTRS = {
	"attrs":{
		"placeholder": "Select Date",
		"_icon": "calendar",
	}
}


RANGE_NAMES = ["Today", "Week", "Month", "Biannual", "Annual"]
DATE_RANGES = {
	"today": lambda x, y: (x, y),
	"week": lambda x, y: (x - timedelta(days=7), y),
	"month": lambda x, y: (x - timedelta(days=30), y),
	"biannual": lambda x, y: (x - timedelta(days=183), y),
	"annual": lambda x, y: (x - timedelta(days=365), y),
}



class DateRangeForm(forms.Form):
	"""
	Form for date ranges.
	"""
	range_names = RANGE_NAMES
	default_date_range = "month"
	date_range = None
	text = None

	f = forms.DateField(
		label="From Date",
		widget=forms.DateInput(**CALENDAR_ATTRS),
		required=False
	)
	
	t = forms.DateField(
		label="To Date",
		widget=forms.DateInput(**CALENDAR_ATTRS),
		required=False
	)


	def __init__(self, data=None, **kwargs):
		"""
		Add date_range field to class.
		Returns inherit parent's __init__() method.
		"""
		if "r" in data:
			self.date_range = data["r"].lower()

		elif "f" in data and "t" in data:
			self.date_range = "custom"

		else:
			self.date_range = self.default_date_range

		return super(__class__, self).__init__(data, **kwargs)


	def get_date_range(self):
		"""
		Return tuple of datetimes.
		"""
		today = date.today()
		tomorrow = today + timedelta(days=1)

		# Set range to default date range if form is invalid
		if not self.is_valid():
			self.date_range = self.default_date_range

		# User specified a named date range
		if self.date_range in DATE_RANGES:
			self.text = self.date_range
			return DATE_RANGES[self.date_range](today, tomorrow)

		# User's custom input values
		self.text = "custom"
		return (self.cleaned_data["f"], self.cleaned_data["t"])