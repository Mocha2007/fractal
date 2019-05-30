import pygame
from math import atan2, isnan, log10, pi
from colorsys import hsv_to_rgb
from inspect import getsourcelines
from time import sleep

inf = float('inf')
nan = float('nan')
black = 0, 0, 0
red = 255, 0, 0

size = 1920, 1080
width, height = size
root_size = 4

graph_width = 2 # how much the screen width is
graph_height = height/width * graph_width# autocalculated
iterations = 50
tolerance = 10**-6
import cmath
function = lambda z: z**3 - 1


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


def get_z_from_coords(coords: (int, int)) -> complex:
	x, y = coords
	real = map_to_range(-graph_width, graph_width, x/width)
	imag = map_to_range(-graph_height, graph_height, (height-y)/height)
	return real+1j*imag


def get_coords_from_z(z: complex) -> (int, int):
	x = map_to_range(0, width, z.real / (2*graph_width) + 1/2)
	y = map_to_range(height, 0, z.imag / (2*graph_height) + 1/2)
	return x, y


def draw_x(coords: (int, int), color: (int, int, int)=black):
	try:
		coords = tuple(round(i) for i in coords)
	except (OverflowError, ValueError):
		return None
	if not (0 < coords[0] < width) or not (0 < coords[1] < width):
		return None
	for i in range(-root_size, root_size+1):
		downward_diagonal_coords = coords[0] - i, coords[1] - i
		screen.set_at(downward_diagonal_coords, color)
		upward_diagonal_coords = coords[0] - i, coords[1] + i
		screen.set_at(upward_diagonal_coords, color)


def plotting(f): # ~40 µs/px avg.
	zeroes = set()
	for x in range(width):
		for y in range(height):
			coords = x, y
			point = get_z_from_coords(coords)
			z, i = newton(f, point)
			color = get_rgb_from_complex(z, i)
			screen.set_at(coords, [int(255*c) for c in color])
			if i < iterations - 1:
				r = int(-log10(tolerance))
				zeroes.add(round(z.real, r) + 1j * round(z.imag, r))
		refresh()
	for zero in zeroes:
		draw_x(get_coords_from_z(zero))
	refresh()

def movie(f, from_val: complex, to_val: complex, frames: int):
	"""Creates a series of images with filename movie/n.png. f is a function which takes a complex number and returns a function to throw into plotting."""
	values = (from_val + i/frames * (to_val - from_val) for i in range(frames))
	for i, value in enumerate(values):
		plotting(f(value))
		pygame.image.save(screen, 'movie/{0}.png'.format(str(i).zfill(5)))

# PYGAME STUFF
pygame.init()
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip
title = 'Newton Fractal'
try:
	title += ' of ' + getsourcelines(function)[0][0]
except TypeError:
	pass
pygame.display.set_caption(title)

# MAIN

# movie(lambda c: lambda z: (z - (-1)**c)*(z - 1j**c)*(z - (-1j)**c), 0, 4, 300)
plotting(function)
pygame.image.save(screen, 'fractal.png')
while 1:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.display.quit()
			pygame.quit()
			exit()
	sleep(.1)
