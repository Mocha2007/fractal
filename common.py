from colorsys import hsv_to_rgb
from math import atan2, isnan, pi

inf = float('inf')
nan = float('nan')

color_convergence = 2
iterations = 20
tolerance = 1e-6

def derivative(f, x: float, n: int=1) -> float:
	# assert 0 < n and type(n) == int
	n -= 1
	if n:
		return derivative(lambda a: derivative(f, a), x, n)
	return (f(x+tolerance) - f(x)) / tolerance

def get_filename(raw_string: str) -> str:
	# invalid chars:
	# \/:*?"<>|
	raw_string = raw_string.replace("lambda ", "f(") \
		.replace(":", ") =") \
		.replace("**", "^") \
		.replace("*", "") \
		.replace("/", "DIV") \
		.replace("\n", "")
	return f'gfx/{raw_string}.png'

def get_rgb_from_complex(z: complex, smoothed: float) -> tuple[float, float, float]:
	if abs(z) == inf:
		return 1, 1, 1
	if isnan(z.real) or isnan(z.imag):
		return 0.5, 0.5, 0.5
	theta = atan2(z.imag, z.real) % (2*pi)
	theta /= 2*pi
	return hsv_to_rgb(theta, 1, smoothed)

def get_rgb_from_i(i: int) -> tuple[float, float, float]:
	return hsv_to_rgb(0, 0, (i/iterations)**(1/color_convergence))

def newton(f, z: complex) -> list[complex]:
	zlist = []
	for _ in range(iterations):
		zlist.append(z)
		try:
			c = f(z)/derivative(f, z)
		except ValueError:
			zlist.append(nan)
			break
		except (OverflowError, ZeroDivisionError):
			# OverflowError, from my experience, usually implies divergence
			zlist.append(inf)
			break
		if abs(c) < tolerance: # converges
			break
		z -= c
	return zlist

def halley(f, z: complex) -> list[complex]:
	zlist = []
	for _ in range(iterations):
		zlist.append(z)
		try:
			c = 2*f(z)*derivative(f, z)/(2*derivative(f, z)**2 - f(z)*derivative(f, z, 2))
		except (OverflowError, ValueError, ZeroDivisionError):
			break
		if abs(c) < tolerance: # converges
			break
		z -= c
	return zlist

def newton_prime(z_: complex) -> list[complex]:
	z = z_ / 3 # average of the three roots
	f = lambda x: (x - z_)*(x*x - 1)
	zlist = []
	for _ in range(iterations):
		zlist.append(z)
		try:
			c = f(z)/derivative(f, z)
		except (OverflowError, ValueError, ZeroDivisionError):
			break
		if abs(c) < tolerance: # converges
			break
		z -= c
	return zlist
