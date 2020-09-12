import sys
import geometry
import numpy as np
import json
import os

def generate_vertices(filename, samples):
	with open(filename) as file:
		raw_parameters = file.read()

	parameters = json.loads(raw_parameters)
	supels = parse_supels(parameters)
	patches = parse_patches(parameters)

	generate_patch_vertices(patches, supels, samples)

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
			'colour': tuple(patch['colour'])
		}

	return patches

def generate_patch_vertices(patches, supels, samples):
	for name, patch in patches.items():
		filename = 'chunk_{}.npy'.format(name)

		if os.path.exists(filename):
			continue

		inner = supels[patch['inner']]
		outer = supels[patch['outer']]
		vertices = geometry.calc_geometry(outer, inner, samples, hint=name)
		chunk = vertices.flatten().astype(np.float32)
		np.save(filename, chunk)

if __name__ == '__main__':
	generate_vertices(sys.argv[1], int(sys.argv[2]))
