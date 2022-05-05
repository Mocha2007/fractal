from colorsys import hsv_to_rgb
from math import atan2, comb, isnan, pi

e2 = 0.57721566490153286 # Euler–Mascheroni constant
inf = float('inf')
nan = float('nan')

color_convergence = 2
iterations = 20
tolerance = 1e-6

_bernoulli_cache = [1, -0.5]
def bernoulli(n: int) -> float:
	if len(_bernoulli_cache) < n: # need lower ones to be filled for cache
		bernoulli(n-1)
	if len(_bernoulli_cache) == n:
		if n % 2:
			_bernoulli_cache.append(0)
		else:
			# https://en.wikipedia.org/wiki/Bernoulli_number#Efficient_computation_of_Bernoulli_numbers
			s = 0
			for k in range(n):
				for v in range(k):
					s += (-1)**v * comb(k, v) * v**n / (k+1)
			_bernoulli_cache.append(s)
	return _bernoulli_cache[n] 

def derivative(f, x: float, n: int=1) -> float:
	# assert 0 < n and type(n) == int
	n -= 1
	if n:
		return derivative(lambda a: derivative(f, a), x, n)
	return (f(x+tolerance) - f(x)) / tolerance

def gamma(z: complex) -> complex:
	"""Weirstass's definition; converges faster than Euler's definition; 0.5% Error @ i"""
	from cmath import exp
	n, g_new, g_old = 0, 1, 0
	while g_new != g_old and n < 100:
		# mag 2.6208191893594548e-05 change after 100 steps with z = 1j
		n += 1
		g_old = g_new
		g_new *= exp(z/n) / (1 + z/n)
	return exp(-e2*z) * g_new / z

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

_zeta_g_n_cache = [e2]
def zeta(z: complex) -> complex:
	# https://en.wikipedia.org/wiki/Riemann_zeta_function#Laurent_series
	if z == 1:
		return inf
	from math import factorial, log
	max_iter = 10
	s = 1/(z-1)
	for n in range(max_iter):
		if len(_zeta_g_n_cache) <= n:
			_zeta_g_n_cache.append(
				sum(log(k)**n / k for k in range(1, max_iter+1))
				- log(max_iter)**(n+1) / (n+1)
			)
		g_n = _zeta_g_n_cache[n]
		s += g_n / factorial(n) * (1-z)**n
	return s
