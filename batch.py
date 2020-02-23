# generate quad tree of images
from PIL import Image
import os
from os.path import exists
import shutil
import subprocess
import solid
import stitch
import downsample
import index
import combine
import deindex

directory = 'temp/images'

def generate_geometry(samples):
	subprocess.run(['python3', 'vertexise.py', str(samples)])

def generate_image(filename, scale, x, y):
	subprocess.run(['python3', 'generate.py', str(scale), str(x), str(y)])
	shutil.move('output.png', filename)

def recursive(stack, scale, x, y, depth):
	if depth == 0:
		return

	path = directory + '/' + '/'.join(stack)

	if not exists(path):
		os.makedirs(path)

	filepath = path + '/image.png'

	if not exists(filepath):
		generate_image(filepath, scale, x, y)
		index.index(filepath)

	# optimisation: further quads of the same colour result in the same image
	if solid.is_solid(filepath):
		return

	recursive(stack[:] + ['tl'], scale * 2, 2 * x + 1, 2 * y + 1, depth - 1)
	recursive(stack[:] + ['tr'], scale * 2, 2 * x - 1, 2 * y + 1, depth - 1)
	recursive(stack[:] + ['bl'], scale * 2, 2 * x + 1, 2 * y - 1, depth - 1)
	recursive(stack[:] + ['br'], scale * 2, 2 * x - 1, 2 * y - 1, depth - 1)

	if depth > 1:
		combine.combine(path)

def clean_images():
	try:
		os.remove('output.png')
	except:
		pass

	try:
		shutil.rmtree(directory)
	except:
		pass

def optimise_image(samples, max_depth, comparable_resolution):
	clean_images()
	generate_geometry(samples)

	# inclusive max_depth
	for depth in range(max_depth + 1):
		if depth == 0:
			continue

		print('Computing image at depth {}'.format(depth))
		# use non-strict-partially-complete tree structure to generate images
		recursive([], 1, 0, 0, depth)
		#stitch.recursive(directory)
		#downsample.downsample(directory + '/stitched.png', comparable_resolution, 'temp/comparable/samples{}depth{}.png'.format(samples, depth))
		#stitch.clean(directory)
		deindex.deindex(directory + '/image.txt', 'temp/comparable/samples{}depth{}.png'.format(samples, depth))

def main():
	optimise_image(1024, 4, 256)

if __name__ == '__main__':
	main()

