from PIL import Image
import sys
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm

def compute_file(filename):
	image = Image.open(filename)
	data = np.array(image)
	mean = np.round(np.mean(data, (0, 1)))

	def compute_metric(samples):
		return np.sum(np.abs(np.round(np.mean(samples, (0, 1))) - mean))

	metrics = [compute_metric(data[x::2,y::2]) for x in range(2) for y in range(2)]

	return metrics

def compute_directory(directory, function):
	samples = 256
	pool = Pool()

	filenames = ['{}/x{}y{}.png'.format(directory, x, y) for x in range(samples) for y in range(samples)]

	print(len(filenames))
	metrics = []

	metrics = pool.map(function, filenames)
	np.savetxt('dump.txt', np.array(metrics))

def generate_error_image():
	image = Image.new('RGB', (256, 256))
	pixels = image.load()
	metrics = np.loadtxt('dump.txt')
	for i, errors in enumerate(metrics):
		accum = np.sum(errors)
		y, x = divmod(i, 256)
		if accum == 0:
			pixels[x, y] = (0, 64, 0)
		else:
			pixels[x, y] = (int(accum * 32), 0, 0)
	image.save('errors.png')

def generate_best_image():
	samples = 256
	image = Image.new('RGBA', (samples, samples))
	pixels = image.load()

	for y in range(samples):
		for x in range(samples):
			print(x, y)
			tile = Image.open('temp/tiles/x{}y{}.png'.format(x, y))
			#median = np.median(np.array(tile), axis=(0, 1))
			mean = np.mean(np.array(tile), axis=(0, 1))
			pixels[x, y] = tuple(map(int, mean))

	image.save('mean256.png')

def max_frequency_difference(filename):
	print(filename)
	image = Image.open(filename)
	data = np.array(image)
	_, counts = np.unique(data.reshape(-1, 4), axis=0, return_counts=True)
	counts.sort()
	if len(counts) >= 2:
		return [counts[-1] - counts[-2], len(counts)]
	return [-1, len(counts)]

generate_best_image()
#compute_directory(sys.argv[1], max_frequency_difference)

#compute_directory(sys.argv[1])

