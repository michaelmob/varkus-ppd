from random import choice
from string import ascii_lowercase, digits


def random(length=5):
	return ''.join([choice(ascii_lowercase + digits) for i in range(length)])
