import pygame
from math import atan2, isnan, pi
from colorsys import hsv_to_rgb
from inspect import getsourcelines

inf = float('inf')
nan = float('nan')
black =   0,   0,   0
white = 255, 255, 255

size = 600, 600
width, height = size

graph_width = 2
iterations = 50
tolerance = 10**-6
function = lambda z: z**(4+3j) - 1


def get_rgb_from_complex(z: complex, i: int) -> (float, float, float):
	if abs(z) == inf or isnan(z.real) or isnan(z.imag):
		return 0.5, 0.5, 0.5
	theta = atan2(z.imag, z.real) % (2*pi)
	theta /= 2*pi
	value = 1 - i / iterations
	return hsv_to_rgb(theta, 1, value)


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
		except (ValueError, ZeroDivisionError):
			return nan, 0
		except OverflowError:
			return z, iterations
		if abs(c) < tolerance: # converges
			break
		z -= c
	return z, i


def map_to_range(start: float, end: float, fraction: float) -> float:
	"""map 0 to start, 1 to end, and intermediate values to linearly between them"""
	return (end-start) * fraction + start


def get_z_from_coords(x: int, y: int) -> complex:
	real = map_to_range(-graph_width, graph_width, x/width)
	imag = map_to_range(-graph_width, graph_width, y/height)
	return real+1j*imag


def plotting(f):
	for x in range(width):
		for y in range(height):
			point = get_z_from_coords(x, height-y)
			z, i = newton(f, point)
			color = get_rgb_from_complex(z, i)
			screen.set_at((x, y), [int(255*c) for c in color])
		refresh()

# PYGAME STUFF
black =   0,   0,   0
white = 255, 255, 255

size = 600, 600
width, height = size

pygame.init()
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip
pygame.display.set_caption('Newton Fractal of ' + getsourcelines(function)[0][0])

# MAIN

plotting(function)
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			exit()
