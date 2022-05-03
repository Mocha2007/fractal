import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Tuple
from common import derivative, get_rgb_from_complex, get_rgb_from_i, inf, iterations, nan, tolerance

graph_width = 2
resolution = 49

# generate point grid
def get_grid() -> np.array:
	a = np.zeros(resolution**2, dtype=complex)
	resolution_axis = np.linspace(-graph_width, graph_width, resolution)
	for i, real in enumerate(resolution_axis):
		for j, imag in enumerate(resolution_axis):
			a[i*resolution+j] = real + imag * 1j
	return a

def newton(f, z: complex) -> Tuple[complex, int]:
	for i in range(iterations):
		try:
			f_ = derivative(f, z)
			if f_ == 0: # no zero
				return inf, 0
			c = f(z)/f_
		except ValueError:
			return nan, 0
		except OverflowError:
			return z, iterations
		if abs(c) < tolerance: # converges
			break
		z -= c
	return z, i

def plotting(f):
	# plotting
	# actual fractal
	plt.subplot(1, 3, 1)
	pointlist = get_grid()
	newtonlist = [newton(f, point) for point in pointlist]
	print(len(list(newtonlist)))
	# zlist, ilist = zip(*newtonlist)
	colorlist = map(lambda x: get_rgb_from_complex(*x), newtonlist)
	scatter1list = list(map(lambda x: x.real, pointlist)), \
		list(map(lambda x: x.imag, pointlist)), \
		colorlist
	plt.scatter(scatter1list[0], scatter1list[1], marker='s', color=list(scatter1list[2]))
	zerolist = [x[0] for x in filter(lambda x: x[1] < iterations-1, newtonlist[::100])]
	plt.scatter(list(map(lambda x: x.real, zerolist)), list(map(lambda x: x.imag, zerolist)), marker='x', color=(0, 0, 0))
	# ...
	plt.title('Newton Fractal')
	plt.xlabel('real')
	plt.ylabel('imag')
	plt.xlim(-graph_width, graph_width)
	plt.ylim(-graph_width, graph_width)

	# iterations
	plt.subplot(1, 3, 2)
	color2list = list(map(lambda x: get_rgb_from_i(x[1]), newtonlist))
	plt.scatter(scatter1list[0], scatter1list[1], marker='s', color=color2list)
	plt.scatter(list(map(lambda x: x.real, zerolist)), list(map(lambda x: x.imag, zerolist)), marker='x', color=(1, 0, 0))
	plt.title('Iterations')
	plt.xlabel('real')
	plt.ylabel('imag')
	plt.xlim(-graph_width, graph_width)
	plt.ylim(-graph_width, graph_width)

	# function plot
	plt.subplot(1, 3, 3)
	x_range = np.linspace(-graph_width, graph_width, 100)
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

plotting(lambda z: z**3 - 2*z + 2)
# plotting(lambda z: z**(4+3j) - 1)
