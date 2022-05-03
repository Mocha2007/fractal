from colorsys import hsv_to_rgb
from math import atan2, isnan, pi
from typing import Tuple

inf = float('inf')
nan = float('nan')

color_convergence = 2
iterations = 50
tolerance = 1e-6

def derivative(f, x: float, n: int=1) -> float:
	assert 0 < n and type(n) == int
	n -= 1
	if n:
		return derivative(lambda a: derivative(f, a), x, n)
	return (f(x+tolerance) - f(x)) / tolerance

def get_rgb_from_complex(z: complex, i: int) -> Tuple[float, float, float]:
	if abs(z) == inf or isnan(z.real) or isnan(z.imag):
		return 0.5, 0.5, 0.5
	theta = atan2(z.imag, z.real) % (2*pi)
	theta /= 2*pi
	value = 1 - i / iterations
	return hsv_to_rgb(theta, 1, value)

def get_rgb_from_i(i: int) -> Tuple[float, float, float]:
	return hsv_to_rgb(0, 0, (i/iterations)**(1/color_convergence))

def newton(f, z: complex) -> Tuple[complex, int]:
	zlist = []
	for i in range(iterations):
		zlist.append(z)
		try:
			f_ = derivative(f, z)
			if f_ == 0: # no zero
				zlist.append(nan)
				break
			c = f(z)/f_
		except (ValueError, ZeroDivisionError):
			zlist.append(nan)
			break
		except OverflowError:
			break
		z -= c
		if abs(c) < tolerance: # converges
			zlist.append(z)
			break
	return zlist
