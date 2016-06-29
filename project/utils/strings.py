from random import choice
from string import ascii_lowercase, digits


def random(length=5):
	return "".join([choice(ascii_lowercase + digits) for i in range(length)])

WORDS = [ "apple", "apricot", "avocado", "banana", "bilberry", "blackberry", "blackcurrant", "blueberry", "boysenberry", "currant", "cherry", "cherimoya", "cloudberry", "coconut", "cranberry", "damson", "date", "dragonfruit", "durian", "elderberry", "feijoa", "fig", "gooseberry", "grape", "raisin", "grapefruit", "guava", "huckleberry", "jabuticaba", "jackfruit", "jambul", "jujube", "kiwifruit", "kumquat", "lemon", "lime", "loquat", "longan", "lychee", "mango", "marionberry", "melon", "cantaloupe", "honeydew", "watermelon", "mulberry", "nectarine", "nance", "olive", "orange", "clementine", "mandarine", "tangerine", "papaya", "peach", "pear", "persimmon", "physalis", "plantain", "plum", "prune", "pineapple", "pomegranate", "pomelo", "quince", "raspberry", "salmonberry", "rambutan", "redcurrant", "salak", "satsuma", "strawberry", "tamarillo", "tamarind", "tomato" ]