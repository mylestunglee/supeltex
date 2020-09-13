import sys
import geometry
import numpy as np
import json
import os
import render
import tqdm
from PIL import Image
from render import buffer_resolution as tile_resolution
import argparse

temp_directory = 'temp'

def generate(
		parameters_filename,
		texture_filename,
		tile_grid_size,
		target_resolution,
		samples,
		processes):
	with open(parameters_filename) as file:
		raw_parameters = file.read()

	parameters = json.loads(raw_parameters)
	supels = parse_supels(parameters)
	patches = parse_patches(parameters)

	if not os.path.exists(temp_directory):
		os.mkdir(temp_directory)

	generate_patch_vertices(patches, supels, samples, processes)
	generate_tiles(patches, tile_grid_size)
	compile_tiles(target_resolution, texture_filename, tile_grid_size)

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

def generate_patch_vertices(patches, supels, samples, processes):
	progress_bar = tqdm.tqdm(total = 2 * len(patches) * samples, desc='preparing')

	for name, patch in patches.items():
		filename = generate_chunk_filename(name)

		if os.path.exists(filename):
			continue

		inner = supels[patch['inner']]
		outer = supels[patch['outer']]
		vertices = geometry.calc_geometry(outer, inner, samples, processes, progress_bar)
		chunk = vertices.flatten().astype(np.float32)
		np.save(filename, chunk)

def generate_tiles(patches, tile_grid_size):
	render.init()

	def generate_tile_at(x, y):
		filename = generate_tile_filename(x, y)

		if os.path.exists(filename):
			return

		offset = tile_grid_size - 1.0
		generate_tile(
			patches,
			float(tile_grid_size),
			offset - 2.0 * x,
			offset - 2.0 * y,
			filename)

	progress_bar = tqdm.tqdm(total = tile_grid_size ** 2, desc='rendering')

	for x in range(tile_grid_size):
		for y in range(tile_grid_size):
			generate_tile_at(x, y)
			progress_bar.update(1)

def generate_tile(patches, scale, offset_x, offset_y, tile_filename):
	geometry_patches = []

	for name, raw_patch in patches.items():
		patch = raw_patch.copy()
		# Set uniforms
		patch['scale'] = scale
		patch['offset'] = (offset_x, offset_y)
		del patch['inner']
		del patch['outer']
		chunk = np.load(generate_chunk_filename(name))
		geometry_patches.append((chunk, patch))

	render.render(geometry_patches, tile_filename)

def compile_tiles(target_resolution, texture_filename, tile_grid_size):
	compile_size = tile_grid_size * tile_resolution
	compiled = Image.new('RGBA', (compile_size, compile_size))

	progress_bar = tqdm.tqdm(total = tile_grid_size ** 2, desc='compiling')

	for x in range(tile_grid_size):
		for y in range(tile_grid_size):
			tile_filename = generate_tile_filename(x, y)
			tile = Image.open(tile_filename)
			compiled.paste(tile, box=(x * tile_resolution, y * tile_resolution))
			progress_bar.update(1)

	resized = compiled.resize((target_resolution, target_resolution), Image.BOX)
	resized.save(texture_filename)

def generate_chunk_filename(name):
	return os.path.join(temp_directory, '{}.npy'.format(name))

def generate_tile_filename(x, y):
	return os.path.join(temp_directory, 'x{}_y{}.png'.format(x, y))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('parameters', help='Parameters defintion filepath')
	parser.add_argument('source_resolution', type=positive_int, help='Supersampled source resolution')
	parser.add_argument('target_resolution', type=positive_int, help='Downscaled target resolution')
	parser.add_argument('-o', '--output', help='Output target image filepath', default='texture.png')
	parser.add_argument('-s', '--samples', type=positive_int, help='Number of samples used in geometry', default=256)
	parser.add_argument('-p', '--processes', type=positive_int, help='Number of processes used in preparation stage', default=1)
	args = parser.parse_args()

	if args.source_resolution < args.target_resolution:
		print('Source resolution must not be smaller than target resolution', file=sys.stderr)
		return

	if not os.path.exists(args.parameters):
		print('Parameters defintion filepath does not exist', file=sys.stderr)
		return

	tile_grid_size = max(1, int(np.ceil(args.source_resolution / tile_resolution)))
	generate(args.parameters, args.output, tile_grid_size, args.target_resolution, args.samples, args.processes)

def positive_int(value):
	parsed = int(value)
	if parsed <= 0:
		raise argparse.ArgumentTypeError('{} is an invalid positive integer value'.format(value))
	return parsed

if __name__ == '__main__':
	main()
