"""Created on Tue Nov 13 14:30:27 2018 @author: Dasharath Adhikari"""

import os
import sys
import pandas as pd 
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True

# file location
path = "/home/dadhikar/Desktop/__CuIr2S4_V2__/Thermal driven study/Thermal noise/text_file/Cooling/time_series/"

# reading data from the file (filename) in file_path
def read_file(filename, a, b):
    x0, x1 = np.loadtxt(path + os.sep+ filename, skiprows=1, usecols=[a,b], unpack=True)
    return x0, x1


t_165K, v_165K = read_file('time_series_165K_2.txt', 0, 1)
t_200K, v_200K = read_file('time_series_200K_1.txt', 0, 1)
t_230K, v_230K = read_file('time_series_230K_1.txt', 0, 1)
t_232K, v_232K = read_file('time_series_232K_1.txt', 0, 1)
t_234K, v_234K = read_file('time_series_234K_1.txt', 0, 1)
t_250K, v_250K = read_file('time_series_250K_1.txt', 0, 1)
t_300K, v_300K = read_file('time_series_300K_1.txt', 0, 1)


# Plotting time series
fig, ax = plt.subplots(1,1, figsize=(10,10), dpi= 250)

ax.plot(t_165K, v_165K-2.5, "C0", label = r"T = 165 K")
#ax.plot(t_200K, v_200K-2, "C1", label = r"T = 200 K")
ax.plot(t_230K, v_230K-1, "C2", label = r"T = 230 K")
ax.plot(t_232K, v_232K+1.2, "C3", label = r"T = 232 K")
ax.plot(t_234K, v_234K+2, "C4", label = r"T = 234 K")
ax.plot(t_250K, v_250K+2.5, "C5", label = r"T = 250 K")
ax.plot(t_300K, v_300K+2.8, "C6", label = r"T = 300 K")

ax.set_xlabel(r't (s)',  fontsize=18)
ax.set_ylabel(r'$\frac{\delta R}{R}[10^{-3}]$ ', fontsize=18)
#ax.set_xlim(0.001,1)
ax.set_ylim(-3, 3)
ax.set_title("Time Series", fontsize= 18)
ax.legend()
ax.set_facecolor('white')
plt.show()