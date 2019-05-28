import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from math import atan2, isnan, pi
from colorsys import hsv_to_rgb

inf = float('inf')
nan = float('nan')


graph_width = 2
max_tolerance = 2**.5 * graph_width
x_range = np.linspace(-graph_width, graph_width, 100)
iterations = 100
resolution = 49
resolution_axis = np.linspace(-graph_width, graph_width, resolution)
tolerance = 10**-5
color_convergence = 2


# generate point grid
def get_grid() -> np.array:
	a = np.zeros(resolution**2, dtype=complex)
	for i, real in enumerate(resolution_axis):
		for j, imag in enumerate(resolution_axis):
			a[i*resolution+j] = real + imag * 1j
	return a


point_grid = get_grid()


def get_rgb_from_complex(z: complex) -> (float, float, float):
	if abs(z) == inf or isnan(z):
		return 0.5, 0.5, 0.5
	theta = atan2(z.imag, z.real) % (2*pi)
	theta /= 2*pi
	return hsv_to_rgb(theta, 1, 1)


def get_rgb_from_i(i: int) -> (float, float, float):
	return hsv_to_rgb(0, 0, (i/iterations)**(1/color_convergence))


def derivative(f, x: float, n: int=1) -> float:
	assert 0 < n and type(n) == int
	n -= 1
	if n:
		return derivative(lambda a: derivative(f, a), x, n)
	return (f(x+tolerance) - f(x)) / tolerance


def newton(f, z: complex) -> (complex, int):
	for i in range(iterations):
		try:
			f_ = derivative(f, z)
			if f_ == 0: # no zero
				return inf, 0
			c = f(z)/f_
		except ValueError:
			return nan, 0
		# if max_tolerance < abs(c): # diverges
		# 	return inf, 0
		if abs(c) < tolerance: # converges
			# print('c')
			break
		z -= c
	# input()
	return z, i


def plotting(f):
	# plotting
	# actual fractal
	plt.subplot(1, 3, 1)
	ilist = []
	zlist = []
	# todo plot roots
	for point in point_grid:
		z, i = newton(f, point)
		ilist.append((point, i))
		zlist.append(z)
		color = get_rgb_from_complex(z)
		plt.scatter(point.real, point.imag, marker='s', color=color)
		plt.scatter(z.real, z.imag, marker='x', color=(0, 0, 0))
	plt.title('Newton Fractal')
	plt.xlabel('real')
	plt.ylabel('imag')
	plt.xlim(-graph_width, graph_width)
	plt.ylim(-graph_width, graph_width)

	# iterations
	plt.subplot(1, 3, 2)
	for (point, i), z in zip(ilist, zlist):
		color = get_rgb_from_i(i)
		plt.scatter(point.real, point.imag, marker='s', color=color)
		plt.scatter(z.real, z.imag, marker='x', color=(1, 0, 0))
	plt.title('Iterations')
	plt.xlabel('real')
	plt.ylabel('imag')
	plt.xlim(-graph_width, graph_width)
	plt.ylim(-graph_width, graph_width)

	# function plot
	plt.subplot(1, 3, 3)
	reals = [f(x).real for x in x_range]
	imags = [f(x).imag for x in x_range]
	plt.plot(x_range, reals, 'b')
	plt.plot(x_range, imags, 'tab:orange')
	plt.plot(x_range, [derivative(f, x).real for x in x_range], 'r')
	plt.plot(x_range, [derivative(f, x, 2).real for x in x_range], 'g')
	# prettification
	plt.title('Function')
	plt.xlabel('x')
	plt.grid()
	plt.xlim(-graph_width, graph_width)
	plt.ylim(min(reals+imags), max(reals+imags))
	# legend
	plt.legend(handles=[
		mpatches.Patch(color='blue', label='f(x)'),
		mpatches.Patch(color='tab:orange', label='Im(f(x))'),
		mpatches.Patch(color='red', label='f′(x)'),
		mpatches.Patch(color='green', label='f″(x)'),
	])

	plt.show()

import cmath
plotting(cmath.sin)