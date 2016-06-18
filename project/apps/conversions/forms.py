from datetime import date, timedelta
from django import forms

DATE_RANGES = {
	"today": 	(date.today(), date.today() + timedelta(days=1)),
	"week": 	(date.today() - timedelta(days=7), date.today()),
	"month": 	(date.today() - timedelta(days=30), date.today()),
	"year": 	(date.today() - timedelta(days=365), date.today())
}

class Form_Conversions_Range(forms.Form):
	t = forms.DateField(label="To Date", required=False)
	f = forms.DateField(label="From Date", required=False)

	def __init__(self, request, **kwargs):
		self.r = request.GET.get("r", None)
		super(__class__, self).__init__(request.GET or None, **kwargs)

	def date_range(self):
		if self.r != None and self.r in DATE_RANGES:
			return DATE_RANGES[self.r]

		if not self.is_valid():
			return None

		return (self.cleaned_data["f"], self.cleaned_data["t"])