# Generates an image of overlapping ellipical shapes using OpenGL shaders

import render
import geometry
import numpy as np
import matplotlib.pyplot as plt
import scipy

parameters_outer = {
	'centre': np.array([0.0, 0.0]),
	'size': np.array([0.8, 1.0]),
	'power': 2.3
}

parameters_refraction = {
	'centre': np.array([0.0, 0.2]),
	'size': np.array([0.64, 0.8]),
	'power': 2
}

parameters_inner = {
	'centre': np.array([0.0, -0.2]),
	'size': np.array([0.2, 0.4]),
	'power': 2.3
}

parameters_centre = {
	'centre': np.array([0.0, -0.2]),
	'size': np.array([0.0, 0.0]),
	'power': 2.3
}

samples = 1000

def calc_renderable_geometry(parameters_1, parameters_2):
	return geometry.calc_geometry(parameters_1, parameters_2, 1000).flatten().astype(np.float32)

geometry_glow = calc_renderable_geometry(parameters_outer, parameters_inner)
geometry_colour = calc_renderable_geometry(parameters_refraction, parameters_inner)
geometry_pupil = calc_renderable_geometry(parameters_inner, parameters_centre)

geometries = [geometry_glow, geometry_colour, geometry_pupil]
fragment_shader_filenames = ['fragment_glow.glsl', 'fragment_colour.glsl', 'fragment_pupil.glsl']

image_size = 1024

render.render(image_size, image_size, geometries, fragment_shader_filenames, 'output.png')
