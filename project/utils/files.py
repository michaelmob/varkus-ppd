import imghdr


def check_image(image):
	return imghdr.what(image.name, image.read(1024))
