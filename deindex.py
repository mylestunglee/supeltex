# converts index text file back into an image

from PIL import Image
import sys
import csv
import numpy as np

def deindex(filename):
	with open(filename, 'r') as file:
		data = np.loadtxt(filename, delimiter=' ', dtype=np.int64)
		size = np.max(data[:, 2])

		image = Image.new('RGBA', (size, size))
		pixels = image.load()
		for row in data:
			x, y, s, r, g, b, a, c = row

			def channelise(z):
				return int(np.round(z / c))

			if s == 1:
				pixels[int(x), int(y)] = tuple([channelise(z) for z in [r, g, b, a]])

		image.save(filename.replace('.txt', '.png'))

def main():
	deindex(sys.argv[1])

if __name__ == '__main__':
	main()
