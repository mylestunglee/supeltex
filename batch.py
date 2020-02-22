# generate quad tree of images
import os
import shutil
import subprocess
import solid

directory = 'temp/images'

def generate(filename, scale, x, y):
	subprocess.run(['python3', 'generate.py', str(scale), str(x), str(y)])
	shutil.move('output.png', filename)

def recursive(stack, scale, x, y, depth):
	if depth == 0:
		return

	path = directory + '/' + '/'.join(stack)
	os.makedirs(path)
	filepath = path + '/image.png'
	generate(filepath, scale, x, y)

	if solid.is_solid(filepath):
		return

	recursive(stack[:] + ['tl'], scale * 2, 2 * x + 1, 2 * y + 1, depth - 1)
	recursive(stack[:] + ['tr'], scale * 2, 2 * x - 1, 2 * y + 1, depth - 1)
	recursive(stack[:] + ['bl'], scale * 2, 2 * x + 1, 2 * y - 1, depth - 1)
	recursive(stack[:] + ['br'], scale * 2, 2 * x - 1, 2 * y - 1, depth - 1)

def main():
	try:
		os.remove('output.png')
	except:
		pass

	try:
		shutil.rmtree(directory)
	except:
		pass

	depth = 5
	recursive([], 1, 0, 0, depth)

if __name__ == '__main__':
	main()
