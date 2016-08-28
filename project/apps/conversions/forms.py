from datetime import date, timedelta
from django import forms

CALENDAR_ATTRS = {
	"attrs":{
		"placeholder": "Select Date",
		"_icon": "calendar",
	}
}

class Form_Conversions_Range(forms.Form):
	f = forms.DateField(label="From Date",
		widget=forms.DateInput(**CALENDAR_ATTRS),required=False)
	t = forms.DateField(label="To Date",
		widget=forms.DateInput(**CALENDAR_ATTRS), required=False)

	@classmethod
	def from_request(cls, request, **kwargs):
		form = cls(request.GET or None, **kwargs)
		form._range = request.GET.get("r", None)
		return form

	def date_range(self):
		today = date.today()
		tomorrow = today + timedelta(days=1)

		if self._range == "month" or not self.is_valid():
			return (today - timedelta(days=30), tomorrow)

		elif self._range == "today":
			return (today, tomorrow)

		elif self._range == "week":
			return (today - timedelta(days=7), tomorrow)

		elif self._range == "year":
			return (today - timedelta(days=365), tomorrow)

		return (self.cleaned_data["f"], self.cleaned_data["t"])