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

path = '/home/dasharath/Desktop/K-TCNQ/voltageDrivenMeasurements/B5S5/082719/time_series/PSD_estimation/'

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
#..............................................................................................
input_file = ['alpha_250K.csv', 'alpha_260K.csv', 'alpha_270K.csv', 'alpha_280K.csv', 'alpha_290K.csv']
#..............................................................................................

v_250, alpha_250, err_alpha_250 = csv_file_read(input_file[0], 0, 1, 2)
v_260, alpha_260, err_alpha_260 = csv_file_read(input_file[1], 0, 1, 2)
v_270, alpha_270, err_alpha_270 = csv_file_read(input_file[2], 0, 1, 2)
v_280, alpha_280, err_alpha_280 = csv_file_read(input_file[3], 0, 1, 2)
v_290, alpha_290, err_alpha_290 = csv_file_read(input_file[4], 0, 1, 2)
fig, ax = plt.subplots(1,1, figsize=(8, 8), facecolor="white", dpi= 150)
ax.errorbar(v_250, alpha_250, yerr= err_alpha_250, fmt='o', lw=0.5, color='C0', markersize=6, alpha=.8, ecolor='black', capsize=5, label='T = 250 K')
ax.errorbar(v_260, alpha_260, yerr= err_alpha_260, fmt='o', lw=0.5, color='C1', markersize=6, alpha=.8, ecolor='black', capsize=5, label='T = 260 K')
ax.errorbar(v_270, alpha_270, yerr= err_alpha_270, fmt='o', lw=0.5, color='C2', markersize=6, alpha=.8, ecolor='black', capsize=5, label='T = 270 K')
ax.errorbar(v_280, alpha_280, yerr= err_alpha_280, fmt='o', lw=0.5, color='C3', markersize=6, alpha=.8, ecolor='black', capsize=5, label='T = 280 K')
ax.errorbar(v_290, alpha_290, yerr= err_alpha_290, fmt='o', lw=0.5, color='C4', markersize=6, alpha=.8, ecolor='black', capsize=5, label='T = 290 K')
ax.set_xlabel(r'V (V)',  fontsize=18)
ax.set_ylabel(r'$\alpha $ (unitless)', fontsize=18)
ax.set_xlim(0, 180)
ax.set_ylim(0.9, 1.8)
ax.set_title(r"Noise study in K-TCNQ_B5S5", fontsize= 15)
ax.set_facecolor('white')
ax.legend(loc='lower center', bbox_to_anchor=(0.8, 0.15), shadow=True, ncol=1, 
            fontsize='small')
#ax.text(0.65, 0.5, r'f = 1 Hz', transform=ax.transAxes, bbox={'facecolor':'skyblue', 'alpha':1.0, 'pad':10})
plt.show()