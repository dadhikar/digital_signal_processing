"""Created on Tue Nov 13 14:30:27 2018 @author: Dasharath Adhikari"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
import os
import sys
import math
from scipy import signal
from scipy import stats
#from file_converter import itx_to_txt_converter
from low_pass_kaiser_window_design import kaiser_FIR, three_stage_decimation

# specifies the location of the raw data    
#path_raw = "/Users/dadhikar/Desktop/rawdata/"
# specifies the file location for the converted text file
input_dir= "/Users/dadhikar/Downloads/Experiment_104/Thermal_noise_D2"
#path_text = "/Users/dadhikar/Desktop/rawdata/"
# Directory for estimted power spectral density
output_dir = "/Users/dadhikar/Downloads/Experiment_104/PSD_cooling"
#path_psd = "/home/dadhikar/Desktop/__CuIr2S4_V2__/Thermal noise/psd/"
# converts igor file from noise measurement into text file
#itx_to_txt_converter(path_raw, path_text)
#sys.exit('stop here!')
#file_list = sorted(os.listdir(input_dir))
#print('-'*25)
#print('The file list: ', file_list)
#print('-'*25)
#sys.exit('stop here!')

file_to_read = input('Enter the name of the file to read data from >>  ')
#reading time, vx and vy from the file 
time, vx, vy = np.loadtxt(input_dir + os.sep + file_to_read, skiprows=1,usecols = [0,1,2], unpack=True)


#Plotting time series
#fig, ax = plt.subplots(1,1, figsize=(5,5), dpi= 150)
#ax.plot(time, vx, c ="r", label = "Signal plus background")
#ax.plot(time, vy, c="g", label= "Background only")
#ax.set_xlabel('t (s)',  fontsize=15)
#ax.set_ylabel(r'$\Delta V (* 10 ^{-6} V) $', fontsize=15)
#ax.set_xlim(0.001,1)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_facecolor('xkcd:salmon')
#ax.legend(loc ='best')
#plt.show()
#sys.exit(-1)  

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
#print(fx)
#sys.exit()
S = abs( Sx - Sy )  # Power spectral density of the sample signal

# Calculating normalized spectrum
vosc = float(input("Enter the value of oscillating voltage >>  "))
Rb = float(input("Enter the value of balancing resistance >>  "))

# Gives the oscillating voltage drop in the sample
vs = vosc/(1 + (1000./Rb))
# Calculates the normalized spectrum density   
S_n = S/vs**2               
# Plotting spectral density
fig, ax = plt.subplots(1,1, figsize=(5, 5), dpi= 150)
ax.loglog(fx, Sx, "ro", label = "PSD (Signal+ background) ")
ax.loglog(fy, Sy, "go", label = "PSD (Background)")
ax.set_xlabel(r'f(Hz)',  fontsize=15)
ax.set_ylabel(r'$ S_{V} (\frac{V^{2}}{Hz})$', fontsize=15)
ax.set_xlim(0.001,10)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.legend()
plt.show()

# calculating the slope_alpha of the PSD
f_list = []
s_list = []
for idx, freq in enumerate(fx):
    if freq > 0.0 and freq <= 1.0:
       f_list.append(freq)
       s_list.append(S_n[idx])
    else:
        continue

f_ = np.asarray(f_list)
s_ = np.asarray(s_list)
#print(f_)
#sys.exit()
slope, intercept, r_value, p_value, std_err = stats.linregress(np.log10(f_), np.log10(s_))
print("."*30)
print(r'The slope {}, standard error {}, and p-value {}'.format(slope, std_err, p_value))
print("."*30)
s_fit = slope*np.log10(f_) + intercept
fig, ax = plt.subplots(1,1, figsize=(5, 5), dpi= 150)
ax.plot(np.log10(f_), np.log10(s_), "go", label = "Normalise PSD")
ax.plot(np.log10(f_), s_fit, color='r', label = r'slope: {} and std_er: {}'.format(round(slope, 3), round(std_err, 3)))
ax.set_xlabel(r"$\log_{10}(f [Hz])$",  fontsize=10)
ax.set_ylabel(r"$\log_{10}(S)$", fontsize=10)
#ax.set_xlim(f.min(), f.max())
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.legend(loc="best")
plt.show()   

# creates the text file of calculated spectral density
psd_file_name = input('Enter the name of the file to store calculated psd >>  ')
FileToWrite = open(output_dir+ os.sep+ psd_file_name, 'w')
FileToWrite.write("f" +"\t"+ "S_n" +"\t"+ "S_fit" +"\t"+ "alpha" +"\t"+ "alpha_er" + "\n" )
for idx, freq in enumerate(f_):
    FileToWrite.write(str(round(freq, 5)) +"\t "+ str(s_[idx]) +'\t'+ 
    str(10**(s_fit[idx])) +'\t'+ str(round(slope,3)) +'\t'+ str(round(std_err, 3))+ '\n')       
FileToWrite.close()

# Plotting normalized-spectral density
fig, ax = plt.subplots(1,1, figsize=(5, 5), dpi= 150)
ax.loglog(f_, f_*s_, "ro", label = "Normalized-PSD")    
ax.set_xlabel(r'$f(Hz)$',  fontsize=15)
ax.set_ylabel(r'$f*\frac{S_{V}}{V^{2}} (\frac{1}{Hz})$', fontsize=15)
ax.set_xlim(0.001,1)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.legend()
plt.show()
    