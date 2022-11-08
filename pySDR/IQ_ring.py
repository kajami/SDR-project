import numpy as np
import scipy
from scipy.signal import resample_poly, firwin, bilinear, lfilter
import matplotlib.pyplot as plt

# Read in signal
x = np.fromfile('fm_rds_250k_1Msamples.iq', dtype=np.complex64)

plt.plot(np.real(x), np.imag(x), '.')
plt.grid(True)
plt.show()