from magic import Magic

image_formats = ["jpg", "jpeg", "png", "bmp", "gif"]


def check_image(image):
	try:
		# a.jpg split by "." is 2
		s = image.name.split(".")
		if len(s) < 2:
			return None

		# Verify the filetype is normal
		if not s[-1].lower() in image_formats:
			return None

		# Add the first 1kb of the file since it removes
		# the 1kb and will corrupt the file
		kb = image.read(1024)

		# If "image" is not in the kb then it's not an image
		magic = Magic()
		if not "image" in str(magic.from_buffer(kb)):
			return None

		return kb + image.read()
	except:
		return None
