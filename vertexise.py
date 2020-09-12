import sys
import geometry
import numpy as np
import json
import os
import render

tile_size = 512

def generate_vertices(parameters_filename='parameters.json', tile_filename='tile.png', samples=1000, threads=8):
	with open(parameters_filename) as file:
		raw_parameters = file.read()

	parameters = json.loads(raw_parameters)
	supels = parse_supels(parameters)
	patches = parse_patches(parameters)

	generate_patch_vertices(patches, supels, samples, threads)
	generate_tile(patches, 1.0, 0.0, 0.0, tile_filename)

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
		filename = 'chunk_{}.npy'.format(name)

		if os.path.exists(filename):
			continue

		inner = supels[patch['inner']]
		outer = supels[patch['outer']]
		vertices = geometry.calc_geometry(outer, inner, samples, threads, name)
		chunk = vertices.flatten().astype(np.float32)
		np.save(filename, chunk)

def generate_tile(patches, scale, offset_x, offset_y, tile_filename):
	geometry_patches = []

	for name, raw_patch in patches.items():
		patch = raw_patch.copy()
		patch['scale'] = scale
		patch['offset'] = (offset_x, offset_y)
		del patch['inner']
		del patch['outer']
		chunk_filename = 'chunk_{}.npy'.format(name)
		chunk = np.load(chunk_filename)
		geometry_patches.append((chunk, patch))

	render.render(tile_size, tile_size, geometry_patches, tile_filename)

if __name__ == '__main__':
	generate_vertices()
