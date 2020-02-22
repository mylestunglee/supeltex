# Determines if a picture has single, uniform colour
from PIL import Image

def is_solid(filename):
	with Image.open(filename) as image:
		width, height = image.size
		pixels = image.load()

		if width == 0 and height == 0:
			raise Exception('Image cannot be empty')

		colour = pixels[0, 0]

		for x in range(width):
			for y in range(height):
				if colour != pixels[x, y]:
					return False

		return True
