PAYMENT_CHOICES = (
	("NONE", "None"),
	("PAYPAL", "Paypal"),
	("CHECK", "Check"),
	("WIRE", "Wire"),
	("DIRECT", "Direct Deposit/ACH"),
)

PAYMENT_ICONS = {
	"NONE": "payment",
	"PAYPAL": "paypal",
	"CHECK": "write",
	"WIRE": "payment",
	"DIRECT": "forward"
}

PAYMENT_CHOICES_DICT = dict(PAYMENT_CHOICES)
PAYMENT_CHOICE_LIST = list(PAYMENT_CHOICES_DICT.keys())
PAYMENT_CHOICE_LIST.remove("NONE")
