#!/usr/bin/env python2

# Author: Enzo De Sena (enzodesena AT gmail DOT com)
# Date: 8/5/2020

import numpy as np


# Testing wrappi
from psr import wrappi
assert(wrappi(0.0) == 0.0)
assert(wrappi(np.pi/10.0) == np.pi/10.0)
assert(wrappi(2.0*np.pi+np.pi/10.0) == np.pi/10.0)
assert(wrappi(-2.0*np.pi+np.pi/10.0) == np.pi/10.0)
assert(wrappi(np.pi+np.pi/10.0) == -np.pi+np.pi/10.0)
assert(wrappi(2.0*np.pi+np.pi+np.pi/10.0) == -np.pi+np.pi/10.0)
assert(wrappi(-2.0*np.pi+np.pi+np.pi/10.0) == -np.pi+np.pi/10.0)


# Testing linear_interpolation
from psr import linear_interpolation
assert(linear_interpolation(1.0, 0.0, 2.0, 1.0, 1.0) == 0.0)
assert(linear_interpolation(1.0, 0.0, 2.0, 1.0, 2.0) == 1.0)
assert(linear_interpolation(1.0, 0.0, 2.0, 1.0, 1.5) == 0.5)


# Testing trig_directivity
from psr import trig_directivity
assert(trig_directivity(np.pi/4, [0.5, 1, 2]) == 0.5+1*np.cos(np.pi/4)+2*np.cos(np.pi/4)**2)
assert(trig_directivity(np.pi/5, [0.5, 1, 2]) == 0.5+1*np.cos(np.pi/5)+2*np.cos(np.pi/5)**2)
assert(trig_directivity(20./180.*np.pi, [ 0.06045714,  0.43903569,  0.41968407]) != trig_directivity(45./180.*np.pi, [ 0.06045714,  0.43903569,  0.41968407]))


# Testing williams_curve_icld
from psr import williams_curve_icld
np.testing.assert_allclose(9.02108371296, williams_curve_icld(0.000312251795545), rtol=1e-10)
np.testing.assert_allclose(14.8185540813, williams_curve_icld(0.), rtol=1e-10)


# All tests passed
print("All tests passed!")
print("-----------------")
print("Next I am asserting false to check asserts are active.")
assert(False)
