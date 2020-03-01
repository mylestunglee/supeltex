import matplotlib.pyplot as plt
import math
import numpy as np

def func(alpha, x):
	return math.sqrt(1.0 - (x / alpha) ** 2.0)

# consider relative to (20, 40) sized ellipse
alpha = 2.0
beta = 1
samples = 1000

def solve(alpha, beta):
	a = 1.0 - 1.0 / (alpha ** 2.0)
	b = 0
	c = 1.0 - 2.0 * alpha ** 2 - beta ** 2.0
	d = 2.0 * alpha ** 2 * beta

	roots = np.roots([a, b, c, d])

	solutions = []
	xroot = 0
	for root in roots:
		if not np.iscomplex(root) and 0.0 <= root <= alpha:
			xroot = root
			x = alpha ** 2.0 / root
			solutions.append(x)
	return solutions, xroot

def gen_circ_points(x, y, r, samples):
	points = []
	for theta in np.linspace(-math.pi, math.pi, samples):
		points.append([x + r * math.cos(theta), y + r * math.sin(theta)])

	return np.array(points)

solutions, xroot = solve(alpha, beta)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')

for x in solutions:
	r = x - beta
	points = gen_circ_points(x, 0, r, samples)
	print('\tfloat radius = {} * 2.0 / 3.0;\n\tfloat upper = {} * 2.0 / 3.0;'.format(r, x))
	ax.plot(points[:, 0], points[:, 1])

X = np.linspace(0, alpha, samples)
Y = [func(alpha, x) for x in X]

ax.plot(X, Y)
plt.xlim(0, alpha)
plt.ylim(0, 1)
plt.show()

'''
def gradient(alpha, x):
	return -x / (alpha ** 2.0 * func(alpha, x))

yroot = func(alpha, xroot)
grad2 = -yroot / (solutions[0] - xroot)
grad1 = gradient(alpha, xroot)

print(grad1, grad2)
'''
