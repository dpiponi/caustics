# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Dimension of image in pixels
N = 256
# Number of samples to use for integration
M = 32
# Magnitude of contour displacement.
# Determined by trial and error with a bunch of contour plots
# of the integrand.
rate = 0.01

# Tabulate Pe(α,β) = ∫(x = -∞,∞) exp(i(x⁴+αx²+β))dx
table = np.zeros((N, N), dtype=np.float64)
xmin, xmax = (-10.0, 10.0)
ymin, ymax = (4.0, -16.0)
alphas = np.linspace(ymin, ymax, N)
betas = np.linspace(xmin, xmax, N)

# Integration range.
# The integrand drops to zero so fast this range
# is fine for now.
x = np.linspace(-4.0, 4.0, M)

for i, alpha in enumerate(alphas):
    for j, beta in enumerate(betas):
        # f(z) = z⁴+αz²+β
        # g(z) = exp(if(z))
        # Instead of integrating along x-axis we're
        # going to integrate along a contour displaced
        # vertically from the x-axis.
        # A good choice of displacement is the gradient
        # d/(Im f(x+iy))/dy.
        # That way, we're displacing in a direction that makes
        # |exp(if(x+iy))| smaller.
        y = rate*(4*x**3+2*alpha*x+beta)
        z = x+1j*y

        f = z**4+alpha*z**2+beta*z
        g = np.exp(1j*f)

        # ∫f(z)dz = ∫f(z)(dz/dx)dx
        dz = 1.0+1j*rate*(12*x**2+2*alpha)
        I = integrate.simps(g*dz, x)

        table[i, j] = np.abs(I)

plt.imshow(table, cmap='gray', extent=[xmin, xmax, ymax, ymin])
plt.title('|Pe(x,y)|')
plt.xlabel('x')
plt.ylabel('y')
plt.colorbar()
plt.show()

# Refs.
# [1] Berry and Klein, Colored diffraction catastrophes
#     http://www.pnas.org/content/93/6/2614.full.pdf
# [2] https://en.wikipedia.org/wiki/Pearcey_integral
