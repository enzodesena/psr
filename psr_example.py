#!/usr/bin/env python2

# Author: Enzo De Sena (enzodesena AT gmail DOT com)
# Date: 8/5/2020
# Please notice that parts of this code are protected by USPTO patent
# H. Hacihabiboglu, E. De Sena, and Z. Cvetkovic, "Microphone array",
# US Patent n. 8,976,977, filed 15/10/2010, granted 10/3/2015.

import numpy as np
import matplotlib.pyplot as plt
from psr import PsrMicrophone
from psr import plot_trig_directivity

# Generates a PSR microphone with radius 15.5 cm and base angle 2pi/5 (74 deg)
mic = PsrMicrophone(0.155, 2*np.pi/5)

# Plots the ideal PSR directivity pattern
mic.plot_directivity()

# Calculates the coefficients of a 2nd-order directivity pattern that best
# approximates the ideal PSR pattern
coeffs = mic.optimal_coefficients(2)
print("Optimal coefficients:")
print(coeffs)

# Overlays the 2nd-order approximation directivity pattern with the ideal one
plot_trig_directivity(coeffs)

# Show plots
plt.show()
