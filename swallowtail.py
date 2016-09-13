# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

# Dimension of image in pixels
N = 256
# Number of samples to use for integration
M = 257
# Magnitude of contour displacement.
# Determined by trial and error with a bunch of contour plots
# of the integrand.
rate = 0.005

# Tabulate Pe(α,β) = ∫(x = -∞,∞) exp(i(z⁵+γz²+βz²+αz))dx
table = np.zeros((N, N), dtype=np.float64)
xmin, xmax = (-20.0, 20.0)
ymin, ymax = (30.0, -20.0)
alphas = np.linspace(ymin, ymax, N)
betas = np.linspace(xmin, xmax, N)

# Integration range.
# The integrand drops to zero so fast this range
# is fine for now.
x = np.linspace(-12.0, 12.0, M)

gammas = np.linspace(0.0, -7.5, 64)
gamma = 0.0
for frame, gamma in enumerate(gammas):
    filename = "image.%04d.png" % frame
    print "Rendering frame", filename
    for i, alpha in enumerate(alphas):
        for j, beta in enumerate(betas):
            # f(z) = z⁵+γz²+βz²+αz
            # g(z) = exp(if(z))
            # Instead of integrating along x-axis we're
            # going to integrate along a contour displaced
            # vertically from the x-axis.
            # A good choice of displacement is proportional
            # to the gradient
            # d/(Im f(x+iy))/dy.
            # That way, we're displacing in a direction that makes
            # |exp(if(x+iy))| smaller.
            # But sometimes that displacement gets too large so I
            # apply a tanh() function to keep it in a reasonable range.
            y = np.tanh(rate*(5*x**4+3*gamma*x**2+2*beta*x+alpha))
            z = x+1j*y

            f = z**5+gamma*z**3+beta*z**2+alpha*z
            g = np.exp(1j*f)

            # ∫f(z)dz = ∫f(z)(dz/dx)dx
            dz = 1.0+1j*rate*(20*x**3+6*gamma*x+2*beta)/np.cosh(rate*(5*x**4+3*gamma*x**2+2*beta*x+alpha))**2
            I = integrate.simps(g*dz, x)

            table[i, j] = np.abs(I)

    plt.imshow(table, cmap='gray', vmin=0.0, vmax=2.8, extent=[xmin, xmax, ymax, ymin])
    plt.title('|Psi(x,y,%1.2f)|' % gamma)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.savefig(filename)
    plt.close()
    plt.show()
