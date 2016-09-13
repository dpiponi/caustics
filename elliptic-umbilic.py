# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.integrate as integrate

# Dimension of image in pixels
N = 129
# Number of samples to use for integration
M = 129
# Magnitude of contour displacement.
# Determined by trial and error with a bunch of contour plots
# of the integrand.
rate = 0.02

# Tabulate Ψ(α,β,γ) = ∫(x,y = -∞,∞) exp(i(x³-3xy²+γ(x²+y²)+αx+βy)dxdy
table = np.zeros((N, N), dtype=np.float64)
xmin, xmax = (-16.0, 16.0)
ymin, ymax = (16.0, -16.0)
alphas = np.linspace(ymin, ymax, N)
betas = np.linspace(xmin, xmax, N)

x0 = np.linspace(-8.0, 8.0, M)
w0 = np.linspace(-8.0, 8.0, M)
(x, w) = np.meshgrid(x0, w0)

# scipy lacks a 2D Simpson integrator so I compute weights
# myself here.
# First compute 1D weights:
wt0 = np.zeros(M, dtype=np.float64)
wt0[0] = 1.0/3.0
wt0[M-1] = 1.0/3.0
wt0[1:M-1:2] = 4.0/3.0
wt0[2:M-2:2] = 2.0/3.0

# And now expand up to 2D weights:
wt = np.outer(wt0, wt0)
h = x0[1]-x0[0]

# This is a 3D function so it'll be a sequence of images over time.
gammas = np.linspace(0.0, 8.0, 64)
for frame, gamma in enumerate(gammas):
    filename = "image.%04d.png" % frame
    print "Rendering frame", filename
    for i, alpha in enumerate(alphas):
        for j, beta in enumerate(betas):
            # z = x+iy
            # u = w+iv
            y = rate*(3*x**2-3*w**2+2*gamma*x+alpha)
            v = rate*(-6*x*w+2*w*gamma+beta)
            z = x+1j*y
            u = w+1j*v

            f = z**3-3*z*u**2+gamma*(z**2+u**2)+beta*u+alpha*z
            g = np.exp(1j*f)

            # ∫f(z, u)dzdu = ∫f(z)(dz/dx)(du/dw)dudw
            dz = 1.0+1j*rate*(6*x+2*gamma)
            du = 1.0+1j*rate*(-6*x+2*gamma)
            I = np.sum(wt*g*dz*du)*h**2

            table[i, j] = np.abs(I)

    plt.imshow(table, cmap='gray', vmin=0.0, vmax=2.7, extent = [xmin, xmax, ymax, ymin])
    plt.title('|Psi(x,y,%1.2f)|' % gamma)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.savefig(filename)
    plt.close()
