# Generates an image of overlapping ellipical shapes using OpenGL shaders

import render
import geometry
import numpy as np
import matplotlib.pyplot as plt
import scipy
from math import pi

def calc_simple_geometry(bottom, top):
	return np.array([
		-1, bottom, -pi, 0,
		1, bottom, pi, 0,
		-1, top, -pi, 1,
		1, top, pi, 1]).astype(np.float32)

geometry_back = np.load('temp/back.npy')
geometry_glow = np.load('temp/glow.npy')
geometry_colour = np.load('temp/colour.npy')
geometry_pupil = np.load('temp/pupil.npy')
#geometry_glow = calc_simple_geometry(-1, 0)
#geometry_colour = calc_simple_geometry(0, 1)

patch_1 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.5,
	'angle_size': (2 * pi) / 12 * 4,
	'polarity_size': 0.5,
	'sharpness': 2.0,
	'shade': (1.0, 0.0, 0.0)
}

patch_2 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.25,
	'angle_size': (2 * pi) / 12 * 4,
	'polarity_size': 0.25,
	'sharpness': 2.0,
	'shade': (0.0, 1.0, 0.0)
}

patch_3 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.25,
	'angle_size': (2 * pi) / 12 * 4,
	'polarity_size': 0.125,
	'sharpness': 2.0,
	'shade': (0.0, 0.0, 1.0)
}

patch_4 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.5,
	'angle_size': 2.0 * pi,
	'polarity_size': 1.0,
	'sharpness': 3.0,
	'shade': (1.0, 1.0, 1.0)
}

patch_5 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.5,
	'angle_size': 2.0 * pi,
	'polarity_size': 1.0,
	'sharpness': 3.0,
	'shade': (0.0, 0.0, 0.0)
}

geometry_patches = [
	(geometry_back, patch_4),
	(geometry_glow, patch_1),
	(geometry_colour, patch_2),
	(geometry_colour, patch_3),
	(geometry_pupil, patch_5)
]

image_size = 256

def append_projection(geometry_patches):
	scale = 1.0
	offset = (0.0, 0.0)

	if len(sys.argv) >= 4:
		scale = float(sys.argv[1])
		offset = (float(sys.argv[2]), float(sys.argv[3]))

	for _, patch in geometry_patches:
		patch['scale'] = scale
		patch['offset'] = offset

append_projection(geometry_patches)

render.render(image_size, image_size, geometry_patches, 'output.png')
