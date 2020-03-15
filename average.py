import numpy as np
from PIL import Image
import sys

def calc_metrics(filename, writer):
	image = Image.open(filename)
	pixels = image.load()

	width = image.size[0]

	accum_all = np.zeros(4)
	accum_tl = np.zeros(4)
	accum_tr = np.zeros(4)
	accum_bl = np.zeros(4)
	accum_br = np.zeros(4)

	for x in range(width):
		for y in range(width):
			pixel = np.array(pixels[x, y])
			accum_all += pixel
			if y % 2 == 0:
				if x % 2 == 0:
					accum_tl += pixel
				else:
					accum_tr += pixel
			else:
				if x % 2 == 0:
					accum_bl += pixel
				else:
					accum_br += pixel

	mean_tl = accum_tl / (width / 2) ** 2
	mean_tr = accum_tr / (width / 2) ** 2
	mean_bl = accum_bl / (width / 2) ** 2
	mean_br = accum_br / (width / 2) ** 2
	mean_all = accum_all / width ** 2

	error_tl = np.abs(mean_tl - mean_all)
	error_tr = np.abs(mean_br - mean_all)
	error_bl = np.abs(mean_bl - mean_all)
	error_br = np.abs(mean_br - mean_all)

	metrics = np.array([error_tl, error_tr, error_bl, error_br])
	np.savetxt(writer, metrics)
	writer.flush()

def calc_all_metrics(directory):
	samples = 256

	with open('metrics.txt', 'wb') as writer:
		for x in range(samples):
			for y in range(samples):
				print(x, y)
				calc_metrics('{}/x{}y{}.png'.format(directory, x, y), writer)

if __name__ == '__main__':
	calc_all_metrics(sys.argv[1])
