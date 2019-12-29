import render
import geometry
import numpy as np
import matplotlib.pyplot as plt
import scipy

points = geometry.calc_geometry(
	{
		'centre': np.array([0, 0]),
		'size': np.array([0.7, 1]),
		'power': 2.4
	},	{
		'centre': np.array([0, -0.3]),
		'size': np.array([0.2, 0.4]),
		'power': 2
	}, 1000)

render.render(2 ** 10, 2 ** 10, points.flatten().astype(np.float32), 'output.png')
