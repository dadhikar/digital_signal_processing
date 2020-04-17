import numpy as np
import scipy
from scipy import signal
x = np.loadtxt('Vt1.txt', usecols=1)
#print(len(x))
window = signal.kaiser(1024, beta=30)
deci_1 =scipy.signal.decimate(x, 4, ftype=window) 
deci_2 =scipy.signal.decimate(deci_1, 2, ftype=window)
y =scipy.signal.decimate(deci_2, 2, ftype='window')
print(y)

