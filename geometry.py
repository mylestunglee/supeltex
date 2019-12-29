import numpy as np
import math
from scipy.optimize import minimize

def signed_power(base, exponent):
	if base < 0:
		return -((-base) ** exponent)
	elif base > 0:
		return base ** exponent
	else:
		return 0

def calc_parametric_point(t, parameters):
	centre = parameters['centre']
	size = parameters['size']
	power = parameters['power']
	x = centre[0] - size[0] * signed_power(math.sin(t), 2 / power)
	y = centre[1] + size[1] * signed_power(math.cos(t), 2 / power)
	return np.array([x, y])

def calc_parametric_distance(t_1, parameters_1, t_2, parameters_2):
	return np.linalg.norm(
		calc_parametric_point(t_1, parameters_1) -
		calc_parametric_point(t_2, parameters_2))

def calc_parametric_dual(t_1, parameters_1, parameters_2, error_tolerance=1e-3):
	def cost_function(t):
		return calc_parametric_distance(t_1, parameters_1, t, parameters_2)

	solution_wrapper = minimize(cost_function,
		t_1,
		method='nelder-mead',
		options={'xatol': error_tolerance, 'disp': False})

	solution = solution_wrapper.x[0]

	# Nomalise solution in [-pi, pi) range
	while solution < -math.pi:
		solution += 2 * math.pi

	while solution >= math.pi:
		solution -= 2 * math.pi

	return solution

def calc_geometry(parameters_1, parameters_2, samples=50):
	def calc_point_1(t):
		point = calc_parametric_point(t, parameters_1)
		return np.array([point[0], point[1], t, 0])

	def calc_point_2(t_1):
		t_2 = calc_parametric_dual(t_1, parameters_1, parameters_2, 1 / (2 * math.pi * samples))
		point = calc_parametric_point(t_2, parameters_2)
		return np.array([point[0], point[1], t_1, 1])

	t_range = np.linspace(-math.pi, math.pi, samples)
	points_1 = np.array([calc_point_1(t) for t in t_range])
	points_2 = np.array([calc_point_2(t) for t in t_range])
	return np.array([point for points in zip(points_1, points_2) for point in points])
