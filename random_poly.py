import pygame
from random import randint, random
from common import newton

black = 0, 0, 0
red = 255, 0, 0

size = 1024, 1024
width, height = size

r_min = -1
r_max = 1
i_min = -1
i_max = 1
degree = 20 # random quadratics
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
	x = map_to_range(0, width, z.real / (2*graph_width) + 1/2)
	y = map_to_range(height, 0, z.imag / (2*graph_height) + 1/2)
	return int(x), int(y)


def heat(coords: tuple[int, int]) -> None:
	current_color = screen.get_at(coords)
	current_color.r += 10
	current_color.g += 10
	current_color.b += 10
	screen.set_at(coords, current_color)


def plotting():
	while 1:
		# generate random polynomial
		c = [randint(-max_coeff_mag, max_coeff_mag) for _ in range(degree+1)]
		f = lambda x: sum(c[i]*x**i for i in range(degree+1))
		# find ONE root of it
		initial_guess = 1j**(4*random())
		r = newton(f, initial_guess)[-1]
		# disp
		coords = get_coords_from_z(r)
		try:
			heat(coords)
		except (IndexError, ValueError):
			continue
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
