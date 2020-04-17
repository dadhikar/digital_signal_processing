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


path = '/home/dasharath/Desktop/K-TCNQ/voltageDrivenMeasurements/B5S4/'

def csv_file_read(filename, a, b, c):
    """
    Reading column of filename using read_csv() 
    and return them
    """
    dataframe = pd.read_csv(path + os.sep+ filename, delimiter=None, header=None, names=None, 
                            index_col=None, usecols=[a, b, c], skiprows=1, skipfooter=0, nrows=None)  
    x1 = dataframe.iloc[:, 0]  
    x2 = dataframe.iloc[:, 1]  
    x3 = dataframe.iloc[:, 2]        
    return x1, x2, x3


def csv_file_read_1(filename, a, b, c, d):
    """
    Reading column 'a' and 'b' in filename using read_csv() 
    and returns the columns data as x and y respectively
    """
    dataframe = pd.read_csv(path + os.sep+ filename, delimiter=None, header=None, names=None, index_col=None, usecols=[a, b, c, d],
                     skiprows=1, skipfooter=0, nrows=None)  
    x1 = dataframe.iloc[:, 0]
    x2 = dataframe.iloc[:, 1] 
    x3 = dataframe.iloc[:, 2]
    x4 = dataframe.iloc[:, 3]                
    return x1, x2, x3, x4

#..............................................................................................
input_file = ['PSD_1Hz_270K.csv', 'PSD_1Hz_280K.csv', 'IV_270K.csv', 'IV_280K.csv']
#..............................................................................................

v_270, psd_270, err_psd_270 = csv_file_read(input_file[0], 0, 1, 2)   
v_280, psd_280, err_psd_280 = csv_file_read(input_file[1], 0, 1, 2) 

I_270K_up, V_270K_up, I_270K_down, V_270K_down  = csv_file_read_1(input_file[2], 0,1,2,3)
I_280K_up, V_280K_up, I_280K_down, V_280K_down  = csv_file_read_1(input_file[3], 0,1,2,3)



fig, ax1 = plt.subplots(1,1, figsize=(8, 8), facecolor="white", dpi= 150)

ax1.plot(V_270K_up, I_270K_up*10**(6), 'o--', c='C0',  label = r"T = 270K (up)")
ax1.plot(V_270K_down, I_270K_down*10**(6), 'o--', c='C1',  label = r"T = 270K (down)")
ax1.set_xlabel(r'V (V)',  fontsize=18)
ax1.set_ylabel(r'I ($\mu$A)', fontsize=18)
#ax1.set_xlim(0.005,10)
#ax.set_ylim(10e-14, 10e-1)
#ax1.set_title(r"Noise study in K-TCNQ", fontsize= 15)
#ax1.set_facecolor('cyan')
#ax1.legend(loc='lower center', bbox_to_anchor=(0.8, 0.85), shadow=True, ncol=2, 
#            fontsize='small')
#ax1.text(0.65, 0.77, r'K-TCNQ_B4S2', transform=ax.transAxes, bbox={'facecolor':'skyblue', 'alpha':1.0, 'pad':10})
#plt.show()

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.errorbar(v_270, psd_270, yerr= err_psd_270, fmt='o--', lw=0.5, color='blue', markersize=6, alpha=.8, ecolor='black', capsize=5, label='f = 1 Hz, T = 270 K')
#ax.errorbar(v_280, psd_280, yerr= err_psd_280, fmt='o--', lw=0.5, color='green', markersize=6, alpha=.8, ecolor='black', capsize=5, label='f = 1 Hz, T = 280 K')

ax2.set_xlabel(r'V (V)',  fontsize=18)
ax2.set_ylabel(r'$\log_{10}(S_{I})[\frac{A^{2}}{Hz}]$', fontsize=18)
#ax.set_xlim(0.005,10)
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title(r"Noise study in K-TCNQ", fontsize= 15)
ax2.set_facecolor('white')
#ax.legend(loc='lower center', bbox_to_anchor=(0.3, 0.85), shadow=True, ncol=1, 
#            fontsize='small')
#ax.text(0.65, 0.77, r'K-TCNQ_B4S2', transform=ax.transAxes, bbox={'facecolor':'skyblue', 'alpha':1.0, 'pad':10})



fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()