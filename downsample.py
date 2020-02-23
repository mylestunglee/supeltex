from PIL import Image
import sys
import numpy as np

# assumes target_size and input_filename's width and height are powers of two
def downsample(input_filename, target_size, output_filename):
	input_image = Image.open(input_filename)
	input_pixels = input_image.load()

	output_image = Image.new('RGBA', (target_size, target_size))
	output_pixels = output_image.load()

	assert input_image.size[0] == input_image.size[1]

	source_size = input_image.size[0]
	cell_size = source_size // target_size

	for x in range(target_size):
		for y in range(target_size):
			# find average pixel
			accum = np.zeros(4)
			for i in range(cell_size):
				for j in range(cell_size):
					accum += np.array(input_pixels[x * cell_size + i, y * cell_size + j])

			pixel = tuple(map(int, np.round(accum / (cell_size * cell_size))))
			output_pixels[x, y] = pixel

	output_image.save(output_filename)

def main():
	downsample(sys.argv[1], int(sys.argv[2]), sys.argv[3])

if __name__ == '__main__':
	main()
