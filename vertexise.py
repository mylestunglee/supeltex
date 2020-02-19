import sys
import geometry
import numpy as np

parameters_outer = {
    'centre': np.array([0.0, 0.0]),
    'size': np.array([20/30, 30/30]),
    'power': 65/30
}

parameters_refraction = {
    'centre': np.array([0, 0/30]),
    'size': np.array([20/30, 25/30]),
    'power': 70/30
}

parameters_inner = {
    'centre': np.array([0, -5/30]),
    'size': np.array([1/4, 1/2]),
    'power': 70/30
}

parameters_centre = {
    'centre': parameters_inner['centre'],
    'size': np.array([0, 0]),
    'power': parameters_inner['power']
}

parameters_back = {
    'centre': np.array([0, 0]),
    'size': np.array([20/30, 40/30]),
    'power': 2
}

if len(sys.argv) > 1:
	samples = int(sys.argv[1])
else:
	samples = 1000



def calc_renderable_geometry(parameters_1, parameters_2):
    return geometry.calc_geometry(parameters_1, parameters_2, samples).flatten().astype(np.float32)

geometry_back = calc_renderable_geometry(parameters_back, parameters_inner)
geometry_glow = calc_renderable_geometry(parameters_outer, parameters_inner)
geometry_colour = calc_renderable_geometry(parameters_refraction, parameters_inner)
geometry_pupil = calc_renderable_geometry(parameters_inner, parameters_centre)

np.save('back.npy', geometry_back)
np.save('glow.npy', geometry_glow)
np.save('colour.npy', geometry_colour)
np.save('pupil.npy', geometry_pupil)
