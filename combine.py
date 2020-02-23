# combine index files from each quad
import sys
import numpy as np

def read_file(filepath):
	return np.loadtxt(filepath, delimiter=' ', dtype=np.int64)

def combine(path):
	data_tl = read_file('{}/tl/image.txt'.format(path))
	data_tr = read_file('{}/tr/image.txt'.format(path))
	data_bl = read_file('{}/bl/image.txt'.format(path))
	data_br = read_file('{}/br/image.txt'.format(path))

	# data in format (x, y, s, r, g, b, a, c)
	width_tl = np.max(data_tl[:, 2])
	width_tr = np.max(data_tr[:, 2])
	width_bl = np.max(data_bl[:, 2])
	width_br = np.max(data_br[:, 2])

	width = max([width_tl, width_tr, width_bl, width_br])

	def calc_scale(width_quad):
		return (width // width_quad) * (width // width_quad)

	with open('{}/image.txt'.format(path), 'w') as text:
		def write_quad(data, offset_x, offset_y):
			for row in data:
				x, y, s, r, g, b, a, c = row

				if s == 1:
					continue

				text.write('{} {} {} {} {} {} {} {}\n'.format(
					x // 2 + offset_x, y // 2 + offset_y, s // 2, r, g, b, a, c))

				if s == width:
					return np.array([r, g, b, a, c], dtype=np.int64)

		half_width = width // 2
		tl = write_quad(data_tl, 0,          0)
		tr = write_quad(data_tr, half_width, 0)
		bl = write_quad(data_bl, 0,          half_width)
		br = write_quad(data_br, half_width, half_width)
		accum = (
			calc_scale(width_tl) * tl +
			calc_scale(width_tr) * tr +
			calc_scale(width_bl) * bl +
			calc_scale(width_br) * br)
		r, g, b, a, c = accum

		text.write('{} {} {} {} {} {} {} {}\n'.format(0, 0, width, r, g, b, a, c))

def main():
	combine(sys.argv[1])

if __name__ == '__main__':
	main()
