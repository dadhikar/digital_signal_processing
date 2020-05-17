"""Initial creation date Tue Nov 13 14:30:27 2018
   @author: Dasharath Adhikari
"""

import os
import sys
import math
from scipy import signal
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
from file_format_converter import itx_to_txt_converter
from low_pass_kaiser_window_design import kaiser_FIR, three_stage_decimation

file_convert = False
# specify the location of the raw data
path_raw = "/Users/dadhikar/Box Sync/CuIr2S4/Experiment_104/"
# specify the file location for the converted text file
path_text = "/Users/dadhikar/Box Sync/CuIr2S4/Experiment_104/Thermal_noise_D2/"
if file_convert:
    print("Converting file format")
    itx_to_txt_converter(path_raw, path_text)

# Directory for estimted power spectral density
output_dir = "/Users/dadhikar/Downloads/Experiment_104/PSD_cooling"

file_list = sorted(os.listdir(path_text))
print('-'*25)
print('The file list: ', file_list)
print('-'*25)

file_to_read = input('Enter the name of the file to read data from >>  ')


# reading time, vx and vy from the file
def read_file(filepath, filename, a, b, c):
    x0, x1, x2 = np.loadtxt(filepath + os.sep + filename, skiprows=1,
                            usecols=[a, b, c], unpack=True)
    return x0, x1, x2


# t = time
# vx = in-phase fluctuation signal
# vy = out-of-phase fluctuation signal
t, vx, vy = read_file(path_text, file_to_read, 0, 1, 2)


# plot the time series if plot is set True
def plot_signal_time_series(time, vx, vy, plot=False):
    if plot:
        # Plotting time series
        fig, ax = plt.subplots(1, 2, figsize=(10, 10), dpi=150)
        # Remove any trend present on  vx and vy fluctuations.
        ax[0].plot(time, vx, c="r", label="Signal + Background")
        ax[0].plot(time, vy, c="g", label="Background only")
        ax[0].set_xlabel(r't (s)',  fontsize=15)
        ax[0].set_ylabel(r'$\delta$V (V)', fontsize=15)
        # ax.set_xlim(0.001,1)
        # ax.set_ylim(10e-14, 10e-1)
        # ax.set_facecolor('xkcd:salmon')
        ax[0].set_title('Signal before detrending')
        ax[0].legend(loc='best')
        vx = signal.detrend(vx, axis=-1, type='linear', bp=0)
        vy = signal.detrend(vy, axis=-1, type='linear', bp=0)
        ax[1].plot(time, vx, c="r", label="Signal + Background")
        ax[1].plot(time, vy, c="g", label="Background only")
        ax[1].set_xlabel(r't (s)',  fontsize=15)
        ax[1].set_ylabel(r'$\delta$V (V)', fontsize=15)
        # ax.set_xlim(0.001,1)
        # ax.set_ylim(10e-14, 10e-1)
        # ax.set_facecolor('xkcd:salmon')
        ax[1].set_title('Signal after detrending')
        ax[1].legend(loc='best')
        plt.show()


plot_signal_time_series(t, vx, vy)

fs = 256.0  # data sampling frequency
D1 = 4.0  # first stage decimation factor
D2 = 2.0  # second stage decimation factor
D3 = 2.0  # third stage decimation factor
decimation_factor = D1*D2*D3
f_pass_final = (0.5/decimation_factor) * fs
print(r'f_sampling = {} Hz, D1= {}, D2= {}, and D3= {}'.format(fs, D1, D2, D3))


# first detrend and do threee stage (antialising + decimation)
# of vx and vy signal
vx = three_stage_decimation(vx, fs, f_pass_final, D1, D2, D3)
vy = three_stage_decimation(vy, fs, f_pass_final, D1, D2, D3)
t_new = np.linspace(start=0, stop=int(t.max()),
                    num=len(vx), endpoint=True)


def plot_decimated_signal_time_series(time, vx, vy, plot=False):
    if plot:
        # Plotting time series
        fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=150)
        # Remove any trend present on  vx and vy fluctuations.
        ax.plot(time, vx, c="r", label="Signal + Background")
        ax.plot(time, vy, c="g", label="Background only")
        ax.set_xlabel(r't (s)',  fontsize=15)
        ax.set_ylabel(r'$\delta$V (V)', fontsize=15)
        # ax.set_xlim(0.001,1)
        # ax.set_ylim(10e-14, 10e-1)
        # ax.set_facecolor('xkcd:salmon')
        ax.set_title('Signal after decimation')
        ax.legend(loc='best')
        plt.show()


plot_decimated_signal_time_series(t_new, vx, vy)

n = len(vx)
# zero padding vx and vy in order to make data, power of 2
n1 = int(np.log2(n))
n1 = np.power(2, n1 + 1)
padding = np.zeros((n1 - n))
vx = np.concatenate((vx, padding))
vy = np.concatenate((vy, padding))

nperseg = 1024*4


def power_spectrum_density(x, spectrum=False):
    """
    Caculate spectral density using Welch periodogram method.
    x : array_like, time series of measurement values
    fs :sampling frequency of the x time series in units of Hz
    window : desired window, defaults to ‘hanning’
    nperseg : length of each segment. Defaults to 256
    noverlap: number of points to overlap between segments
    If None, noverlap = nperseg / 2
    nfft : Length of the FFT used, if a zero padded FFT is desired
    If None, the FFT length is nperseg. Defaults to None.
    detrend: specifies how to detrend each segment. defaults to ‘constant’.
    return_onesided : bool,if True, return a one-sided spectrum for real data
    if False return a two-sided spectrum
    scaling : { ‘density’, ‘spectrum’ }, optional
    """
    if spectrum:
        f, S = signal.welch(x, fs=fs/(D1*D2*D3), window='hann',
                            nperseg=nperseg, noverlap=0.5*nperseg, nfft=None,
                            detrend='constant', return_onesided=True,
                            scaling='spectrum', axis=-1)
    else:
        f, S = signal.welch(x, fs=fs/(D1*D2*D3), window='hann',
                            nperseg=nperseg, noverlap=0.5*nperseg, nfft=None,
                            detrend='constant', return_onesided=True,
                            scaling='density', axis=-1)
    return f, S


# spectral density estimation from vx data
fx, Sx = power_spectrum_density(vx)
# spectral density estimation form vy data
fy, Sy = power_spectrum_density(vy)


def psd_plot(fx, Sx, fy, Sy, plot=True):
    if plot:
        # Plotting time series
        fig, ax = plt.subplots(1, 1, figsize=(10, 10), dpi=150)
        # Remove any trend present on  vx and vy fluctuations.
        ax.loglog(fx, Sx, c="r", label="PSD (signal + background)")
        ax.loglog(fy, Sy, c="g", label="Background only")
        ax.set_xlabel(r'f [Hz]',  fontsize=15)
        ax.set_ylabel(r'S$_{v}$ [$\frac{V^{2}}{Hz}$]', fontsize=15)
        # ax.set_xlim(0.001,1)
        # ax.set_ylim(10e-14, 10e-1)
        # ax.set_facecolor('xkcd:salmon')
        ax.set_title('Power Spectral Density')
        ax.legend(loc='best')
        plt.show()


psd_plot(fx, Sx, fy, Sy)
sys.exit()


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
    