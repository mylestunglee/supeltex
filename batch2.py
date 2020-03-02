from PIL import Image
import batch
from os.path import exists

def main():
	#batch.generate_geometry(
	tiles = 8
	offset = 1 - tiles
	for x in range(tiles):
		for y in range(tiles):
			name = 'temp/tiles/x{}y{}.png'.format(x, y)
			if not exists(name):
				batch.generate_image(name, tiles, -(2*x + offset), -(2*y + offset))

	source_size = 256
	target_size = source_size * tiles
	stitched = Image.new('RGBA', (target_size, target_size))
	for x in range(tiles):
		for y in range(tiles):
			name = 'temp/tiles/x{}y{}.png'.format(x, y)
			tile = Image.open(name)
			stitched.paste(tile, box=(x * source_size, y * source_size))
	stitched.save('temp/tiles/stitched.png')

if __name__ == '__main__':
	main()
