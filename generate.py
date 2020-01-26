# Generates an image of overlapping ellipical shapes using OpenGL shaders

import render
import geometry
import numpy as np
import matplotlib.pyplot as plt
import scipy

parameters_outer = {
	'centre': np.array([0.0, 0.0]),
	'size': np.array([2/3, 1]),
	'power': 7/3
}

parameters_refraction = {
	'centre': np.array([0, 0]),
	'size': np.array([0.6, 0.75]),
	'power': 7/3
}

parameters_inner = {
	'centre': np.array([0, -1/3]),
	'size': np.array([0.2, 0.75-1/3]), # 3/4-1/3=9/12-4/12=5/12
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

geometry_glow = calc_renderable_geometry(parameters_outer, parameters_inner)
geometry_colour = calc_renderable_geometry(parameters_refraction, parameters_inner)
geometry_pupil = calc_renderable_geometry(parameters_inner, parameters_centre)

geometries = [geometry_glow, geometry_colour, geometry_pupil]
fragment_shader_filenames = ['fragment_glow.glsl', 'fragment_colour.glsl', 'fragment_pupil.glsl']

image_size = 512

render.render(image_size, image_size, geometries, fragment_shader_filenames, 'output.png')
