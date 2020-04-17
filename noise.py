"""Created on Tue Nov 13 14:30:27 2018 @author: Dasharath Adhikari"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import sys
import math
from scipy import signal

from file_converter import itx_to_txt_converter
from Kaiser_Window_Design import Kaiser_FIR, Three_Stage_Decimation

# specifies the location of the raw data    
path_raw = "/Users/dadhikar/Desktop/rawdata/"
# specifies the file location for the converted text file
path_text = "/Users/dadhikar/Desktop/rawdata/"
# Directory for estimted power spectral density
path_psd = "/home/dadhikar/Desktop/__CuIr2S4_V2__/Thermal noise/psd/"
# converts igor file from noise measurement into text file
itx_to_txt_converter(path_raw, path_text)
#sys.exit('stop here!')

#file_list = sorted(os.listdir(path_text))
#print('-'*25)
#print('The file list: ', file_list)
#print('-'*25)

print('Enter the name of the file to read data from: ')
file_to_read = input()
print('-'*25)
#reading time, vx and vy from the file 
time, vx, vy = np.loadtxt(path_text+os.sep+file_to_read, skiprows=1,usecols = [0,1,2], unpack=True)

# Remove any trend present on  vx and vy fluctuations.
vx = signal.detrend(vx, axis=-1, type='linear', bp=0)
vy = signal.detrend(vy, axis=-1, type='linear', bp=0)

"""
FileToWrite = open(path_text + os.sep + 'time_series.txt', 'w')
FileToWrite.write('t' +'\t'+ 'Vx' +'\t'+ 'Vy' + '\n')
for i in range(len(time)):
    if time[i] > 100.0:
        continue
    else:
        FileToWrite.write(str(time[i]) +'\t'+ str(vx[i]) +'\t'+ str(vy[i]) + '\n')
    
FileToWrite.close()   
"""


#Plotting time series
fig, ax = plt.subplots(1,1, figsize=(7,7), dpi= 150)
ax.plot(time, vx, c ="r", label = r"Signal plus background")
ax.plot(time, vy, c="g", label= r"Background only")
ax.set_xlabel('t (s)',  fontsize=15)
ax.set_ylabel(r'$\Delta V (* 10 ^{-6} V) $', fontsize=15)
#ax.set_xlim(0.001,1)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.set_facecolor('xkcd:salmon')
ax.set_facecolor((1.0, 0.47, 0.42))
ax.legend()
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
plt.show()
#sys.exit(-1)  

# Getting vx (signal + background) and vy (background only) after decimation
vx = Three_Stage_Decimation(vx)
vy = Three_Stage_Decimation(vy)
t  = np.linspace(0,len(vx)*(1/16), len(vx), True)

# Zero padding to make data power of 2
n = len(vx)
pads = [0.0] * int(math.pow(2, int(math.log(n,2)) +1) -n)
vx = vx.tolist()
vx += pads
vx = np.asarray(vx)
vy = vy.tolist()
vy += pads
vy = np.asarray(vy)

# Caculating spectral density using Welch periodogram method. I am calling the module signal from
# Scipy library in Python
def Power_Spectrum_Density(x):
    f, S = signal.welch(x, fs=16, window='hann', nperseg=4096,  noverlap=0.75* 4096, nfft=None, 
                           detrend='constant', return_onesided=True, scaling='density', axis=-1)
    return f, S

# Here I am calculating spectrum not density using same method as above
def Power_Spectrum(x):
    f, S = signal.welch(x, fs=16, window='hann', nperseg=4096,  noverlap=0.75* 4096, nfft=None, 
                           detrend='constant', return_onesided=True, scaling='spectrum', axis=-1)
    return f, S

# spectral density estimation from vx data
fx, Sx = Power_Spectrum_Density(vx) 
# spectral density estimation form vy data
fy, Sy = Power_Spectrum_Density(vy)

S = abs( Sx - Sy )  # Power spectral density of the sample signal

# Calculating normalized spectrum
print("Enter the value of oscillating voltage: ")
print('-'*25)
vosc = float(input())
print('-'*25)
print("Enter the value of balancing resistance: ")
print('-'*25)
Rb = float(input())
print('-'*25)

# Gives the oscillating voltage drop in the sample
vs = vosc/(1 + (1000./Rb))
# Calculates the normalized spectrum density   
S_n = S/vs**2               
# Plotting spectral density
fig, ax = plt.subplots(1,1, figsize=(7, 7), dpi= 150)
ax.loglog(fx, Sx, "ro", label = "PSD (Signal+ background) ")
ax.loglog(fy, Sy, "go", label = "PSD (Background)")
ax.set_xlabel(r'f(Hz)',  fontsize=15)
ax.set_ylabel(r'$ S_{V} (\frac{V^{2}}{Hz})$', fontsize=15)
ax.set_xlim(0.001,10)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.legend()
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
plt.show()
    
# Plotting normalized-spectral density
fig, ax = plt.subplots(1,1, figsize=(7, 7), dpi= 150)
ax.loglog(fx, S_n, "ro", label = "Normalized-PSD")    
ax.set_xlabel(r'$f(Hz)$',  fontsize=15)
ax.set_ylabel(r'$\frac{S_{V}}{V^{2}} (\frac{1}{Hz})$', fontsize=15)
ax.set_xlim(0.001,10)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.legend()
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
plt.show()
    


# creates the text file of calculated spectral density
print('Enter the name of the file to store calculated psd: ')
print('-'*25)
psd_file_name = input()
print('-'*25)
FileToWrite = open(path_psd + os.sep+ psd_file_name, 'w')
FileToWrite.write("frequency" + "\t " + "Sx" + "\t " + "Sy" + "\t "+
                  "S(=Sx-Sy)" +"\t"+ "S(normalized)" +"\n" )
for i in range(len(fx)):
    if i == 0:
        continue
    else:
        FileToWrite.write(str(fx[i]) +"\t "+ str(Sx[i]) +"\t "+ str(Sy[i]) 
        +"\t "+ str(S[i]) +"\t "+ str(S_n[i]) +"\n")    
FileToWrite.close()

