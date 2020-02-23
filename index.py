# gets an image and makes indices in the form of (x, y, size, red, green, blue, alpha, count)
from PIL import Image
import numpy as np
import sys

def recursive(pixels, text, x, y, s):
	if s == 1:
		r, g, b, a = pixels[x, y]
		c = 1
		text.write('{} {} {} {} {} {} {} {}\n'.format(x, y, s, r, g, b, a, c))
		return np.array([r, g, b, a, c])

	tl = recursive(pixels, text, x, y, s // 2)
	tr = recursive(pixels, text, x + s // 2, y, s // 2)
	bl = recursive(pixels, text, x, y + s // 2, s // 2)
	br = recursive(pixels, text, x + s // 2, y + s // 2, s // 2)

	accum = tl + tr + bl + br
	r, g, b, a, c = accum
	text.write('{} {} {} {} {} {} {} {}\n'.format(x, y, s, r, g, b, a, c))

	return accum

def index(filename):
	image = Image.open(filename)
	pixels = image.load()
	width = image.size[0]

	text = open(filename.replace('.png', '.txt'), 'w')

	recursive(pixels, text, 0, 0, width)

def main():
	index(sys.argv[1])

if __name__ == '__main__':
	main()
