import sys
import geometry
import numpy as np
import json
import os
import render
import tqdm
from PIL import Image

tile_resolution = 512
tile_grid_size = 16

def generate(
		parameters_filename='parameters.json',
		tile_filename='tile.png',
		target_resolution=1024,
		samples=1000,
		threads=8):
	with open(parameters_filename) as file:
		raw_parameters = file.read()

	parameters = json.loads(raw_parameters)
	supels = parse_supels(parameters)
	patches = parse_patches(parameters)

	if not os.path.exists('temp'):
		os.mkdir('temp')

	generate_patch_vertices(patches, supels, samples, threads)
	generate_tiles(patches)
	compile_tiles(target_resolution)

def parse_supels(parameters):
	supels = {}

	for name, supel in parameters['supels'].items():
		supels[name] = {
			'centre': np.array(supel['centre']),
			'size': np.array(supel['size']),
			'power': supel['power']
		}

	return supels

def parse_patches(parameters):
	patches = {}

	for name, patch in parameters['patches'].items():
		patches[name] = {
			'inner': patch['inner'],
			'outer': patch['outer'],
			'angle_centre': patch['angle_centre'],
			'angle_size': patch['angle_size'],
			'polarity_centre': patch['polarity_centre'],
			'polarity_size': patch['polarity_size'],
			'sharpness': patch['sharpness'],
			'shade': tuple(patch['shade'])
		}

	return patches

def generate_patch_vertices(patches, supels, samples, threads):
	for name, patch in patches.items():
		filename = 'temp/{}.npy'.format(name)

		if os.path.exists(filename):
			continue

		inner = supels[patch['inner']]
		outer = supels[patch['outer']]
		vertices = geometry.calc_geometry(outer, inner, samples, threads, 'preparing geometry for {}'.format(name))
		chunk = vertices.flatten().astype(np.float32)
		np.save(filename, chunk)

def generate_tiles(patches):
	render.init(tile_resolution, tile_resolution)

	def generate_from_pair(pair):
		x, y = pair
		filename = 'temp/x{}_y{}.png'.format(x, y)

		if not os.path.exists(filename):
			offset = 1 - tile_grid_size
			generate_tile(
				patches,
				float(tile_grid_size),
				-(2.0 * x + offset),
				-(2.0 * y + offset),
				filename)

	pairs = [(x, y) for x in range(tile_grid_size) for y in range(tile_grid_size)]

	for pair in tqdm.tqdm(pairs, desc='rendering'):
		generate_from_pair(pair)

def generate_tile(patches, scale, offset_x, offset_y, tile_filename):
	geometry_patches = []

	for name, raw_patch in patches.items():
		patch = raw_patch.copy()
		# Set uniforms
		patch['scale'] = scale
		patch['offset'] = (offset_x, offset_y)
		del patch['inner']
		del patch['outer']
		chunk_filename = 'temp/{}.npy'.format(name)
		chunk = np.load(chunk_filename)
		geometry_patches.append((chunk, patch))

	render.render(tile_resolution, tile_resolution, geometry_patches, tile_filename)

def compile_tiles(target_resolution):
	compile_size = tile_grid_size * tile_resolution
	stitched = Image.new('RGBA', (compile_size, compile_size))
	for x in range(tile_grid_size):
	        for y in range(tile_grid_size):
	                name = 'temp/x{}_y{}.png'.format(x, y)
	                tile = Image.open(name)
	                stitched.paste(tile, box=(x * tile_resolution, y * tile_resolution))
	stitched.save('temp/stitched.png')

if __name__ == '__main__':
	generate()
