#!/usr/bin/env python2

# Author: Enzo De Sena (enzodesena AT gmail DOT com)
# Date: 8/5/2020
# Please notice that parts of this code are protected by USPTO patent
# H. Hacihabiboglu, E. De Sena, and Z. Cvetkovic, "Microphone array",
# US Patent n. 8,976,977, filed 15/10/2010, granted 10/3/2015.

import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import minimize

def linear_interpolation(x0, y0, x1, y1, x):
    m = (y1-y0)/(x1-x0)
    return y0+(x-x0)*m


def wrappi(angle):
    wrapped_angle = angle % (2.0*np.pi)
    if wrapped_angle > np.pi:
        wrapped_angle = wrapped_angle - 2.0*np.pi
    return wrapped_angle


def williams_curve_icld(tau_max):
    # This is a generalised logistic approximation of Williams curve
    icld_max = 221.5913-230.1794/(1.0+np.exp(-(tau_max*1000.0+2.1786)))
    return icld_max


def trig_directivity(angle, coefficients):
    value = 0.0
    for i, coeff in enumerate(coefficients):
        value = value + coeff * np.cos(angle)**i
    return value


def trig_directivity_vec(angles, coefficients):
    dirpattern = np.zeros(len(angles))
    for n, angle in enumerate(angles):
        dirpattern[n] = trig_directivity(angle, coefficients);
    return dirpattern


def plot_directivity(angles, directivity_values):
    plt.polar(angles, 20.0*np.log10(np.abs(directivity_values)+0.001))
    plt.ylim(top=0.0,bottom=-25.0)


def plot_trig_directivity(coefficients, num_points = 1000):
    angles = np.linspace(-np.pi, np.pi, num_points)
    directivity_values = trig_directivity_vec(angles, coefficients)
    plot_directivity(angles, directivity_values)

class PsrMicrophone:
    def __init__(self, array_radius, base_angle):
        self.array_radius = array_radius
        self.base_angle = base_angle
        self.grace_angle = np.pi/15
        self.lambda_value = 0.5
        self.sound_speed = 343.


    def get_gamma(self, theta):
        tau_max = 2.*self.array_radius/self.sound_speed*np.sin(self.base_angle/2.) * np.sin(self.base_angle/2.)
        icld_max = williams_curve_icld(tau_max)
        
        # In the multichannel's paper reference system, eta_db is negative
        eta_db = -icld_max

        # Convert to dBs
        eta = 10. ** (eta_db/20.)
        beta = np.arctan((eta*np.sin(self.base_angle)) / (1.-eta*np.cos(self.base_angle)))

        phi = np.sin(theta-(0.-beta)) / np.sin((self.base_angle+beta)-theta)
        gamma = (1.+phi**2.)**(-0.5);

        return gamma


    def get_directivity(self, theta):
        # The remainder of the code assumes angles are between 0 and pi
        # so we now transform to that range using wrappi
        theta = abs(wrappi(theta))
        if theta < self.base_angle or theta > 2.*np.pi-self.base_angle:
            return self.get_gamma(theta)
        elif (theta < (self.base_angle+self.grace_angle)):
            return linear_interpolation(
                self.base_angle,
                self.get_gamma(self.base_angle),
                self.base_angle+self.grace_angle,
                0.,
                theta);
        elif (theta > (2.*np.pi-self.base_angle-self.grace_angle)):
            return linear_interpolation(
                2.*np.pi-self.base_angle-self.grace_angle,
                0., 2.*np.pi-self.base_angle,
                self.get_gamma(2.*np.pi-self.base_angle-self.grace_angle),
                theta)
        else:
            return 0.


    def calculate_directivity(self):
        self.thetas = np.linspace(0., 2*np.pi, num=5000, endpoint=True)
        self.dirpattern = np.zeros(len(self.thetas))
        for i, theta in enumerate(self.thetas):
            self.dirpattern[i] = self.get_directivity(theta) / self.get_directivity(0)


    def plot_directivity(self):
        self.calculate_directivity()
        plot_directivity(self.thetas, self.dirpattern)


    def cost_function(self, coefficients):
        # Add coefficient
        coefficients = np.insert(coefficients, 0, 1.-sum(coefficients))

        delta = self.thetas[1] - self.thetas[0]
        thetas_in_range = (self.thetas > 0) & (self.thetas < self.base_angle)
        fit_in_range = sum((self.dirpattern[thetas_in_range] -
            trig_directivity_vec(self.thetas[thetas_in_range], coefficients))**2) * delta

        thetas_out_of_range = (self.thetas > (self.base_angle + self.grace_angle)) & (self.thetas < np.pi)
        fit_out_of_range = sum(trig_directivity_vec(self.thetas[thetas_out_of_range], coefficients)**2) * delta

        return self.lambda_value * fit_in_range + (1.-self.lambda_value) * fit_out_of_range


    def optimal_coefficients(self, order):
        # Start with omnidirectional directivity
        x0 = np.zeros(order)
        x0[0] = 1.

        res = minimize(self.cost_function, x0, method='nelder-mead', tol=1e-10) # , options={'disp': True}
        coefficients = np.insert(res.x, 0, 1.-sum(res.x))
        return coefficients
