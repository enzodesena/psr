# Perceptual Soundfield Reconstruction (PSR)
Python module to generate Perceptual Soundfield Reconstruction (PSR) directivity patterns and its higher-order approximations as described in: E. De Sena, H. Hacıhabiboğlu, and Z. Cvetković, "Analysis and Design of Multichannel Systems for Perceptual Sound Field Reconstruction," IEEE Trans. on Audio, Speech and Language Process., vol. 21 , no. 8, pp 1653-1665, Aug. 2013.


**Please notice that parts of this code are protected by USPTO patent H. Hacihabiboglu, E. De Sena, and Z. Cvetkovic, "Microphone array", US Patent n. 8,976,977, filed 15/10/2010, granted 10/3/2015.**
**If you'd like to use this software for any reason other than non-commercial research purposes, please contact enzodesena AT gmail DOT com**


## Getting Started

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

## Example

```python
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
```

## Running the tests

Run `python psr_tests.py`.


## Authors

The work to develop PSR was carried out by E. De Sena, H. Hacıhabiboğlu, and Z. Cvetković while they were at King's College London (UK) with support by EPSRC Grant EP/F001142/1, and was published in: 
E. De Sena, H. Hacıhabiboğlu, and Z. Cvetković, "Analysis and Design of Multichannel Systems for Perceptual Sound Field Reconstruction," IEEE Trans. on Audio, Speech and Language Process., vol. 21 , no. 8, pp 1653-1665, Aug. 2013.

The python software was written by Enzo De Sena while a Lecturer (Assistan Professor) at the University of Surrey. 

* **Enzo De Sena** - [desena.org](https://desena.org)


## License

This project is licensed under the GNU GPL v3.0 License - see the [LICENSE](LICENSE) file for details. Also notice that parts of the code are protected under USPTO patent n. 8,976,977.
