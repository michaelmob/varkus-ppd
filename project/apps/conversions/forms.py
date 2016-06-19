from datetime import date, timedelta
from django import forms


class Form_Conversions_Range(forms.Form):
	f = forms.DateField(label="From Date", required=False)
	t = forms.DateField(label="To Date", required=False)

	def __init__(self, request, **kwargs):
		self.r = request.GET.get("r", None)
		super(__class__, self).__init__(request.GET or None, **kwargs)

	def date_range(self):
		today = date.today()
		tomorrow = today + timedelta(days=1)

		if self.r == "month" or not self.is_valid():
			return (today - timedelta(days=30), tomorrow)

		elif self.r == "today":
			return (today, tomorrow)

		elif self.r == "week":
			return (today - timedelta(days=7), tomorrow)

		elif self.r == "year":
			return (today - timedelta(days=365), tomorrow)

		return (self.cleaned_data["f"], self.cleaned_data["t"])