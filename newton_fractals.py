import numpy as np
import matplotlib.pyplot as plt
from math import atan2, pi
from colorsys import hsv_to_rgb

x_range = np.linspace(-2, 2, 100)
iterations = 100
resolution = 30
resolution_axis = np.linspace(-2, 2, resolution)
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
		f_ = derivative(f, z)
		if f_ == 0:
			return z
		c = f(z)/f_
		# print(z, c)
		if abs(c) < tolerance: # converges
			# print('c')
			break
		if 2 < abs(c): # diverges
			# print('d')
			i = 0
			z = float('inf')
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

	# iterations
	plt.subplot(1, 3, 2)
	for (point, i), z in zip(ilist, zlist):
		color = get_rgb_from_i(i)
		plt.scatter(point.real, point.imag, marker='s', color=color)
		plt.scatter(z.real, z.imag, marker='x', color=(1, 0, 0))
	plt.title('Iterations')
	plt.xlabel('real')
	plt.ylabel('imag')

	# function plot
	plt.subplot(1, 3, 3)
	plt.plot(x_range, f(x_range), 'b')
	plt.plot(x_range, [derivative(f, x) for x in x_range], 'r')
	plt.plot(x_range, [derivative(f, x, 2) for x in x_range], 'g')
	plt.title('Function')
	plt.grid()

	plt.show()

plotting(lambda z: z**3 - 2*z + 2)