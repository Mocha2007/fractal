import pygame
from math import log
from common import get_rgb_from_complex, iterations, newton_prime, tolerance

black = 0, 0, 0
red = 255, 0, 0

size = 1024, 1024
width, height = size

r_min = 0.75
r_max = 0.9
i_min = 0.75
i_max = 0.9

def smoothing(zlist: list[complex]) -> float:
	i = len(zlist)
	try:
		z0, z1, root = zlist[-3:]
		ld0 = log(abs(z0 - root))
		ld1 = log(abs(z1 - root))
		correction = (log(tolerance) - ld0)/(ld1 - ld0)
		value = 1 - (i + 0.5*correction)/iterations
		return min(1, max(0, value))
	except ValueError:
		return 1 - i/iterations


def map_to_range(start: float, end: float, fraction: float) -> float:
	"""map 0 to start, 1 to end, and intermediate values to linearly between them"""
	return (end-start) * fraction + start


def get_z_from_coords(coords: tuple[int, int]) -> complex:
	x, y = coords
	real = map_to_range(r_min, r_max, x/width)
	imag = map_to_range(i_min, i_max, (height-y)/height)
	return real+1j*imag


def plotting():
	for x in range(width):
		for y in range(height):
			coords = x, y
			point = get_z_from_coords(coords)
			zlist = newton_prime(point)
			color = get_rgb_from_complex(zlist[-1], smoothing(zlist))
			screen.set_at(coords, [int(255*c) for c in color])
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
title = 'Newton Prime Fractal'
pygame.display.set_caption(title)

# MAIN

# movie(lambda c: lambda z: (z - (-1)**c)*(z - 1j**c)*(z - (-1j)**c), 0, 4, 300)
plotting()
pygame.image.save(screen, 'fractal.png')
