import pathos.multiprocessing as mp
import numpy as np
from scipy.optimize import minimize
import math

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def signed_power(base, exponent):
    if base < 0:
        return -((-base) ** exponent)
    if base > 0:
        return base ** exponent
    return 0


def calc_parametric_point(t, parameters):
    centre = parameters['centre']
    size = parameters['size']
    power = parameters['power']
    angle = 0

    if 'angle' in parameters:
        angle = parameters['angle']

    x = centre[0] - size[0] * signed_power(math.sin(t), 2 / power)
    y = centre[1] + size[1] * signed_power(math.cos(t), 2 / power)

    x2, y2 = rotate(centre, (x, y), -np.radians(angle))

    return np.array([x2, y2])


def calc_parametric_distance(t_1, parameters_1, t_2, parameters_2):
    return np.linalg.norm(
        calc_parametric_point(t_1, parameters_1) -
        calc_parametric_point(t_2, parameters_2))


def calc_parametric_dual(t_1, parameters_1, parameters_2):
    # t_2 parameter is independent of distance if parameters_2 represents a dot
    if not parameters_2['size'].any():
        return t_1

    def cost_function(t):
        return calc_parametric_distance(t_1, parameters_1, t, parameters_2)

    solution_wrapper = minimize(cost_function,
                                t_1,
                                method='nelder-mead',
                                options={'xatol': 0, 'disp': False, 'maxiter': 2**8})

    solution = solution_wrapper.x[0]

    # Nomalise solution in [-pi, pi) range
    while solution < -np.pi:
        solution += 2 * np.pi

    while solution >= np.pi:
        solution -= 2 * np.pi

    return solution


def calc_geometry(parameters_1, parameters_2, samples=50, processes=8, progress_bar=None):
    def calc_point_1(t):
        point = calc_parametric_point(t, parameters_1)
        return np.array([point[0], point[1], t, 0])

    def calc_point_2(t_1):
        t_2 = calc_parametric_dual(
            t_1, parameters_1, parameters_2)
        point = calc_parametric_point(t_2, parameters_2)
        return np.array([point[0], point[1], t_1, 1])

    def calc_point(pair):
        polarity, t = pair

        if not polarity:
            return calc_point_1(t)

        return calc_point_2(t)

    with mp.ProcessingPool(processes) as pool:
        t_range = np.linspace(-np.pi, np.pi, samples)
        pair_range = [(polarity, t)
                      for t in t_range for polarity in [False, True]]
        points = []

        for point in pool.imap(calc_point, pair_range):
            progress_bar.update(1)
            points.append(point)

        pool.close()

    return np.array(points)
