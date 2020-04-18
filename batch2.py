from PIL import Image
import batch
from os.path import exists
import multiprocessing
import time
import downsample

tiles = 16

offset = 1 - tiles
def generate_image(pair):
	x, y = pair
	name = 'temp/tiles/x{}y{}.png'.format(x, y)
	print(name)
	if not exists(name):
		batch.generate_image(name, tiles, -(2*x + offset), -(2*y + offset))

def main():
	pool = multiprocessing.Pool(4)
	pairs = [(x, y) for x in range(tiles) for y in range(tiles)]
	pool.map(generate_image, pairs)

	source_size = 512
	target_size = source_size * tiles

	stitched = Image.new('RGBA', (target_size, target_size))
	for x in range(tiles):
		for y in range(tiles):
			name = 'temp/tiles/x{}y{}.png'.format(x, y)
			tile = Image.open(name)
			stitched.paste(tile, box=(x * source_size, y * source_size))
	stitched.save('temp/tiles/stitched.png')
	downsample.downsample('temp/tiles/stitched.png', 512, 'mean{}.png'.format(tiles))

if __name__ == '__main__':
	main()
