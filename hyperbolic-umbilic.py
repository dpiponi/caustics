# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.integrate as integrate

# Dimension of image in pixels
N = 128
# Number of samples to use for integration
M = 65
# Magnitude of contour displacement.
# Determined by trial and error with a bunch of contour plots
# of the integrand.
rate = 0.02

# Tabulate Ψ(α,β,γ) = ∫(x,y = -∞,∞) exp(i(x³-3xy²+γ(x²+y²)+αx+βy)dxdy
table = np.zeros((N, N), dtype=np.float64)
umin, umax = (-8.4*np.cbrt(3.0), 8.4*np.cbrt(3.0))
vmin, vmax = (4.2*np.cbrt(3.0), -12.7*np.cbrt(3.0))
us = np.linspace(umin, umax, N)
vs = np.linspace(vmin, vmax, N)

s0 = np.linspace(-6.0, 6.0, M)
t0 = np.linspace(-6.0, 6.0, M)
S0, T0 = np.meshgrid(s0, t0)

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
h = s0[1]-s0[0]

# This is a 3D function so it'll be a sequence of images over time.
zs = np.linspace(0.0, 3.0, 128)
for frame, z in enumerate(zs):
    filename = "image.%04d.png" % frame
    print "Rendering frame", filename
    for i, v in enumerate(vs):
        for j, u in enumerate(us):
            x = (v-u)/np.sqrt(2.0)
            y = (u+v)/np.sqrt(2.0)
            S1 = rate*(3*S0**2+z*T0+x)
            T1 = rate*(3*T0**2+z*S0+y)

            S = S0+1j*S1
            T = T0+1j*T1

            f = S**3+T**3+z*S*T+y*T+x*S
            g = np.exp(1j*f)

            # ∫f(z, u)dzdu = ∫f(z)(dz/dx)(du/dw)dudw
            dz = 1.0+1j*rate*(6*S0)
            du = 1.0+1j*rate*(6*T0)
            I = np.sum(wt*g*dz*du)*h**2

            table[i, j] = np.abs(I)

    plt.imshow(table, cmap='gray', vmin=0.0, vmax=5.0, extent = [umin, umax, vmax, vmin])
    plt.title('|Psi(x,y,%1.2f)|' % z)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.colorbar()
    plt.savefig(filename)
    plt.close()
