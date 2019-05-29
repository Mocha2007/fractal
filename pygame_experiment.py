import pygame

black =   0,   0,   0
white = 255, 255, 255

size = 800, 600
width, height = size

pygame.init()
screen = pygame.display.set_mode(size)
refresh = pygame.display.flip

# MAIN
screen.fill(black)
for x in range(width):
	for y in range(height):
		screen.set_at((x, y), white)
	refresh()
