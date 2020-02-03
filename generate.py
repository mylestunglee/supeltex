# Generates an image of overlapping ellipical shapes using OpenGL shaders

import render
import geometry
import numpy as np
import matplotlib.pyplot as plt
import scipy
from math import pi

parameters_outer = {
	'centre': np.array([0.0, 0.0]),
	'size': np.array([5/6, 1]),
	'power': 13/6
}

parameters_refraction = {
	'centre': np.array([0, 0]),
	'size': np.array([2/3, 2/3]),
	'power': 7/3
}

parameters_inner = {
	'centre': np.array([0, -1/6]),
	'size': np.array([1/3, 1/3]),
	'power': 7/3
}

parameters_centre = {
	'centre': parameters_inner['centre'],
	'size': np.array([0, 0]),
	'power': parameters_inner['power']
}

samples = 1000

def calc_renderable_geometry(parameters_1, parameters_2):
	return geometry.calc_geometry(parameters_1, parameters_2, 1000).flatten().astype(np.float32)

def calc_simple_geometry(bottom, top):
	return np.array([
		-1, bottom, -pi, 0,
		1, bottom, pi, 0,
		-1, top, -pi, 1,
		1, top, pi, 1]).astype(np.float32)

geometry_glow = calc_renderable_geometry(parameters_outer, parameters_inner)
geometry_colour = calc_renderable_geometry(parameters_refraction, parameters_inner)
geometry_pupil = calc_renderable_geometry(parameters_inner, parameters_centre)
#geometry_glow = calc_simple_geometry(-1, 0)
#geometry_colour = calc_simple_geometry(0, 1)

patch_1 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.5,
	'angle_size': (2 * pi) / 12 * 4,
	'polarity_size': 0.5,
	'sharpness': 2.0,
	'shade': (1.0, 0.0, 0.0, 1.0)
}

patch_2 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.25,
	'angle_size': (2 * pi) / 12 * 4,
	'polarity_size': 0.25,
	'sharpness': 2.0,
	'shade': (0.0, 1.0, 0.0, 1.0)
}

patch_3 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.25,
	'angle_size': (2 * pi) / 12 * 4,
	'polarity_size': 0.125,
	'sharpness': 2.0,
	'shade': (0.0, 0.0, 1.0, 1.0)
}

patch_4 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.5,
	'angle_size': 2.0 * pi,
	'polarity_size': 1.0,
	'sharpness': 3.0,
	'shade': (1.0, 1.0, 1.0, 1.0)
}

patch_5 = {
	'angle_centre': 0.0,
	'polarity_centre': 0.5,
	'angle_size': 2.0 * pi,
	'polarity_size': 1.0,
	'sharpness': 3.0,
	'shade': (0.0, 0.0, 0.0, 1.0)
}

geometry_patches = [
	(geometry_glow, patch_4),
	(geometry_glow, patch_1),
	(geometry_colour, patch_2),
	(geometry_colour, patch_3),
	(geometry_pupil, patch_5)
]

image_size = 512

render.render(image_size, image_size, geometry_patches, 'output.png')
