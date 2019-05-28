import numpy as np
import matplotlib.pyplot as plt
from math import atan2, pi
from colorsys import hsv_to_rgb

x_range = np.linspace(-2, 2, 100)
iterations = 100
resolution = 20
resolution_axis = np.linspace(-2, 2, resolution)
tolerance = 10**-5


# generate point grid
def get_grid() -> np.array:
	a = np.zeros(resolution**2, dtype=complex)
	for i, real in enumerate(resolution_axis):
		for j, imag in enumerate(resolution_axis):
			a[i*resolution+j] = real + imag * 1j
	return a


point_grid = get_grid()


def get_rgb_from_complex(z: complex) -> (int, int, int):
	theta = atan2(z.imag, z.real) % (2*pi)
	theta /= 2*pi
	return hsv_to_rgb(theta, 1, 1)


def derivative(f, x: float, n: int=1) -> float:
	assert 0 < n and type(n) == int
	n -= 1
	if n:
		return derivative(lambda a: derivative(f, a), x, n)
	return (f(x+tolerance) - f(x)) / tolerance


def newton(f, z: complex) -> complex:
	for _ in range(iterations):
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
			z = float('inf')
			break
		z -= c
	# input()
	return z


def plotting(f):
	# plotting
	# actual fractal
	plt.subplot(1, 2, 1)
	for point in point_grid:
		z = newton(f, point)
		plt.scatter(point.real, point.imag, color=get_rgb_from_complex(z))
	plt.title('Newton Fractal')
	plt.xlabel('real')
	plt.ylabel('imag')

	# function plot
	plt.subplot(1, 2, 2)
	plt.plot(x_range, f(x_range), 'b')
	plt.plot(x_range, [derivative(f, x) for x in x_range], 'r')
	plt.plot(x_range, [derivative(f, x, 2) for x in x_range], 'g')
	plt.title('Function')

	plt.show()

plotting(lambda z: z**3 - 2*z + 2)