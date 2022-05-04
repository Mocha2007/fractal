import pygame
from random import randint, random
from common import newton

white = 255, 255, 255

size = 1024, 1024
width, height = size

r_min = 0
r_max = 2
i_min = 0
i_max = 2
degree = 24 # random quadratics
max_coeff_mag = 1

graph_width = r_max - r_min
graph_height = i_max - i_min


def exit_program() -> None:
	pygame.image.save(screen, f'poly{degree}-{max_coeff_mag}.png')
	pygame.display.quit()
	pygame.quit()
	exit()


def map_to_range(start: float, end: float, fraction: float) -> float:
	"""map 0 to start, 1 to end, and intermediate values to linearly between them"""
	return (end-start) * fraction + start


def get_coords_from_z(z: complex) -> tuple[int, int]:
	x = map_to_range(0, width, z.real / graph_width)
	y = map_to_range(height, 0, z.imag / graph_height)
	return int(x), int(y)


def heat(coords: tuple[int, int]) -> None:
	screen.set_at(coords, white)


def fourfold_symmetry(z: complex) -> None:
	_z = abs(z.real) + 1j*abs(z.imag)
	coords = get_coords_from_z(_z)
	try:
		heat(coords)
	except (IndexError, OverflowError, ValueError):
		pass


def plotting():
	while 1:
		# generate random polynomial
		c = [(-1)**randint(0, 1) for _ in range(degree+1)]
		f = lambda x: sum(c[i]*x**i for i in range(degree+1))
		# find ONE root of it
		initial_guess = 1j**(4*random())
		r = newton(f, initial_guess)[-1]
		# disp
		fourfold_symmetry(r)
		refresh()
		# check if exiting
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit_program()

# PYGAME STUFF
pygame.init()
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip
title = 'Newton Prime Fractal'
pygame.display.set_caption(title)

# MAIN

plotting()
