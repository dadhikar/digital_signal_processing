"""
Author @ Dasharath Adhikari
"""
import os
import sys
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import seaborn as sb
sb.set(context='notebook', style='ticks', palette='bright', font='sans-serif', font_scale = 1.5,
       color_codes =True, rc=None)
sb.color_palette(palette=None, n_colors=None, desat=None)

path = '/home/dasharath/Desktop/K-TCNQ/voltageDrivenMeasurements/B4S2/time_series/PSD_estimation/'

v , PSD_ttl = np.loadtxt(path +os.sep+ "PSD_SUM.txt", skiprows=1, usecols = [0,1], unpack=True)
alpha = np.loadtxt(path +os.sep+ "alpha.txt", skiprows=1, usecols = 1, unpack=True)


# Plotting total spectral density and alpha
fig, ax1 = plt.subplots(1,1, figsize=(7,7), facecolor="white", dpi= 200)
ax1.semilogy(v, PSD_ttl, '-o', color='r', label = r"PSD total")
ax1.set_xlabel(r'V (V)',  fontsize=18)
ax1.set_ylabel(r'$\log_{10}$(S$_{I}$)[A$^{2}$]', fontsize=18)
ax1.set_facecolor('cyan')
ax1.legend()
ax1.legend(loc='lower center', bbox_to_anchor=(0.2, 0.8), shadow=False, ncol=1,  
           fontsize='small')
ax1.set_title(r"Noise study in K-TCNQ", fontsize= 15)
ax1.text(0.4, 0.8, r'K-TCNQ_B4S2', transform=ax1.transAxes, bbox={'facecolor':'skyblue', 'alpha':0.8, 'pad':10})

ax2 = ax1.twinx()
ax2.plot(v, alpha, '-o', color='g', label = r"$\alpha$")
ax2.set_ylabel(r'$\alpha$', fontsize=20)
ax2.legend(loc='lower center', bbox_to_anchor=(0.15, 0.7), shadow=False, ncol=1,  
           fontsize='small')    
plt.show()