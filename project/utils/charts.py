from datetime import timedelta, date


def today_range():
	return {"date_time__range": [date.today(), date.today() + timedelta(days=1)]}


def convert_number(n):
	if((n == 0) or (n > 23)):
		return str("12a")
	elif(n == 23):
		return str("11p")
	elif(n == 12):
		return str("12p")
	elif(n < 13):
		return str(n) + "a"
	else:
		return str(int(n - 12)) + "p"


def hour_chart_lead_count(objects):
	chart = ""
	chart_dict = {x: 0 for x in range(24)}

	for obj in objects:
		chart_dict[(obj.date_time).hour] += 1

	for key, value in chart_dict.items():
		chart += "[\"%s\", %s]," % (key, value)

	return chart[:-1]


def hour_chart(objects, cut_amount=0):
	chart = ""
	chart_dict = {x: [0.0, 0] for x in range(24)}

	for obj in objects:
		key = (obj.date_time).hour
		# If already exists just add onto the payment
		if key in chart_dict:
			chart_dict[key][0] += float(obj.user_payout)
		else:  # Otherwise add the payment to the dict
			chart_dict[key][0] = float(obj.user_payout)

		chart_dict[(obj.date_time).hour][1] += 1

	for key, value in chart_dict.items():
		chart += "[\"%s\", %s, %s]," % (key, value[0], value[1])

	return chart[:-1]


def map_chart(objects):
	chart = ""
	chart_dict = {}

	for obj in objects:
		# If already exists just add onto the payment
		if obj.country in chart_dict:
			chart_dict[obj.country][0] += float(obj.user_payout)
			chart_dict[obj.country][1] += 1
		else:  # Otherwise add the payment to the dict
			chart_dict[obj.country] = [float(obj.user_payout), 1]

	for key, value in chart_dict.items():
		chart += "[\"%s\", %s, %s]," % (key, value[0], value[1])

	return chart[:-1]
