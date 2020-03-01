# compare two images
from functools import cmp_to_key
import sys
import os
from PIL import Image
import numpy as np
import plotly.express as px

def sum_errors(filename1, filename2):
	image1 = Image.open(filename1)
	image2 = Image.open(filename2)
	pixels1 = image1.load()
	pixels2 = image2.load()

	width, _ = image1.size

	errors = 0

	for y in range(width):
		for x in range(width):
			r1, g1, b1, a1 = pixels1[x, y]
			r2, g2, b2, a2 = pixels2[x, y]

			errors += abs(r2 - r1)
			errors += abs(g2 - g1)
			errors += abs(b2 - b1)
			errors += abs(a2 - a1)

	return errors

def compare_names(name1, name2):
	def tokenise(name):
		return name.replace('samples', '').replace('depth', ' ').replace('.png', '').split()

	samples1, depth1 = [int(token) for token in tokenise(name1)]
	samples2, depth2 = [int(token) for token in tokenise(name2)]

	if samples1 < samples2 or samples1 == samples2 and depth1 < depth2:
		return -1

	if samples1 > samples2 or samples1 == samples2 and depth1 > depth2:
		return 1

	return 0

def generate_matrix():
	directory = sys.argv[1]
	files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
	files = sorted(files, key=cmp_to_key(compare_names))
	print(' '.join(files))
	for file1 in files:
		for file2 in files:
			print(sum_errors(os.path.join(directory, file1), os.path.join(directory, file2)), '', end='', flush=True)
		print()

def main():
	data = np.loadtxt('dump2.txt')
	fig = px.imshow(data)
	fig.show()

if __name__ == '__main__':
	main()
