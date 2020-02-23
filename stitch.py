from os.path import exists
from PIL import Image
import sys
import subprocess
import shutil

# stitch images
def recursive(path):
	quads = ['tl', 'tr', 'bl', 'br']

	for quad in quads:
		child = path + '/' + quad
		if exists(child):
			recursive(child)

	if all(exists(path + '/' + quad) for quad in quads):
		images = []
		for quad in quads:
			if exists(path + '/' + quad + '/stitched.png'):
				images.append(Image.open(path + '/' + quad + '/stitched.png'))
			else:
				raise Exception('Cannot find ' + quad + ' in path ' + path)

		width = max(images[i].size[0] for i, _ in enumerate(quads))

		# we want to stitch images of different sizes
		for i, quad in enumerate(quads):
			if images[i].size[0] != width:
				# resample method is not important because images[i] is a solid colour
				images[i] = images[i].resize((width, width), resample=Image.NEAREST)

		stitched = Image.new('RGBA', (width * 2, width * 2))
		stitched.paste(im=images[0], box=(0, 0))
		stitched.paste(im=images[1], box=(width, 0))
		stitched.paste(im=images[2], box=(0, width))
		stitched.paste(im=images[3], box=(width, width))
		stitched.save(path + '/stitched.png')
	else:
		shutil.copyfile(path + '/image.png', path + '/stitched.png')

def clean(path):
	subprocess.run(['find', path, '-type', 'f', '-name', '*stitched.png' '-delete'])

def main():
	recursive(sys.argv[1])

if __name__ == '__main__':
	main()
