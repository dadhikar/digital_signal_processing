""" Created on Tue Apr  2 13:18:39 2019 @author: dasharath"""

import sys
import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
import math
from scipy.fftpack import ifft
from Kaiser_Window_Design import Three_Stage_Decimation


# Specifying the path for the file
file_path = "/home/dadhikar/Desktop/__CuIr2S4_V2__/Thermal driven study/Thermal noise/text_file/Cooling/"
file_path1 = '/home/dadhikar/Desktop/__CuIr2S4_V2__/Thermal driven study/Thermal noise/text_file/Cooling/uncorrupted_time_series/'
# reading data from the file (filename) in file_path
def read_file(filename, a, b, c):
    x0, x1, x2 = np.loadtxt(file_path + os.sep+ filename, skiprows=1, usecols=[a,b,c], unpack=True)
    return x0, x1, x2

# --------------------------------------------------------------------------------------------------  
file = input("Enter the file name to read data from:  ")
# --------------------------------------------------------------------------------------------------

t, dvx, dvy = read_file(file, 0, 1, 2)

# remove any trend present on  vx and vy fluctuations.
dvx = signal.detrend(dvx, axis=-1, type='linear', bp=0)
dvy = signal.detrend(dvy, axis=-1, type='linear', bp=0)

# dvx (signal + background) and dvy (background only) after decimation
dvx = Three_Stage_Decimation(dvx)
dvy = Three_Stage_Decimation(dvy)

# spectral density estimation using Welch periodogram method
def Power_Spectrum_Density(x):
    f, S = signal.welch(x, fs=16, window='hann', nperseg=4096,  noverlap=0.75* 4096, nfft=None, 
                           detrend='constant', return_onesided=True, scaling='density', axis=-1)
    return f, S

n = len(dvx)
pads = [0.0] * int(math.pow(1, int(math.log(n,2)) +1) -n) # Zero padding to make data power of 2
dvx = dvx.tolist()
dvx += pads
dvx = np.asarray(dvx)
dvy = dvy.tolist()
dvy += pads
dvy = np.asarray(dvy)

fx, Sx = Power_Spectrum_Density(dvx)
fy, Sy = Power_Spectrum_Density(dvy)

# Plotting power spectral density
def Spectral_Plot(a,b,c,d):
    fig, ax = plt.subplots(1,1, figsize=(5, 5), dpi= 200)
    ax.loglog(a, b, "ro", label = "Signal + background")
    ax.loglog(c, d, "ko", label="Background")
    ax.set_xlabel(r'$f (Hz)$',  fontsize=10)
    ax.set_ylabel(r'$\frac{S_{v}}{V^{2}}(\frac{1}{Hz})$', fontsize=10)
    #ax.set_xlim(0.001,1)
    #ax.set_ylim(10e-14, 10e-1)
    #ax.set_title("")
    ax.legend()
    plt.show()
    
#Spectral_Plot(fx, Sx, fy, Sy)
#sys.exit()

f = []
for i in range(len(fx)):
    if fx[i] <= 1:
        f.append(fx[i])         
    else: 
        continue
f = np.asarray(f)
# Caculating transfer function of the Wiener filter
TF = (Sx[0:len(f)] - Sy[0:len(f)])/Sx[0:len(f)]
#plt.scatter(f, TF)  
#TF = TF * np.exp(-1j*2*np.pi/len(TF)*np.arange(len(TF))*(len(TF)//2))  # shift for causal filter
pads = [0.0] * int(math.pow(2, int(math.log(len(TF),2)) +1) -len(TF))
TF =TF.tolist()
TF += pads
TF = np.asarray(TF)
TF = ifft(TF, n= None, axis = -1, overwrite_x = False)
TF = abs(TF)
dvx_uncor = np.convolve(dvx, TF, mode='same')
list_vx = []
for i in range(len(dvx_uncor)):
    if dvx_uncor[i] == 0.0:
        continue
    else:
        list_vx.append(dvx_uncor[i])
dvx_uncor = np.asarray(list_vx)        
time = np.linspace(0,len(dvx_uncor)*(1/16), len(dvx_uncor), True)
# plotting uncorrupted time series
plt.plot(time, dvx_uncor, label ='Uncorrupted')
plt.legend()
plt.show()
# --------------------------------------------------------------------------------------------------
# Writing uncorrupted voltage fluctuation in a file
file1 = input("Name the file to write uncorrupted time series data:   ")
# --------------------------------------------------------------------------------------------------
FileToWrite = open(file_path1+ os.sep +  file1, 'w')
FileToWrite.write('time' +"\t"+ 'vx_uncor' + "\n")
 
for i in range(len(dvx_uncor)):
    FileToWrite.write(str(time[i]) +'\t'+ str(dvx_uncor[i]) + "\n")
FileToWrite.close()    
    