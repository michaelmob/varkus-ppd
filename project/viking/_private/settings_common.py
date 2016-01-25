DEBUG = True

# Deposits # Default must exist // Always make "-1" default
DEPOSITS = (
	# User ID   Company     Aff ID      Deposit Code        Deposit Name        Password
	(-1,		"COMPANY",	1,			"DEFAULT_DEPOSIT",	"Default Deposit",	"PASSWORD"),
)

DEPOSIT_NAMES = ((d[3], d[4],) for d in DEPOSITS)
POSTBACK_PASSWORD = DEPOSITS[0][5]
DEFAULT_AFFILIATE_ID = DEPOSITS[0][2]
