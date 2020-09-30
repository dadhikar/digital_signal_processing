"""
Author @ Dasharath Adhikari
"""
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
pathin = " "
pathout = " "

# reading data from the file (filename) in file_path
def read_file(filename, a, b):
    x0, x1 = np.loadtxt(pathin + os.sep+ filename, skiprows=1, usecols=[a,b], unpack=True)
    return x0, x1



def csv_file_read(filename, a):
    """
    Reading column of filename using read_csv() 
    and return them
    """
    dataframe = pd.read_csv(pathin + os.sep+ filename, delimiter=None,
                            header=None, names=None, index_col=None,
                            usecols=[a], skiprows=1, skipfooter=0, nrows=None)  
    x1 = dataframe.iloc[:, 0]           
    return x1 


#.......................................................................
file = input("Name the input file with format:  ") # enter the file name
#.......................................................................

t, dvx = read_file(file, 0, 1)

# detrending the voltage fluctuation time series
dvx = signal.detrend(dvx, type='linear')

# creating new file and write i  and t 
#........................................................................
filename = input("Name the output file with format:  ") # enter the file name
#........................................................................
file1 = open(pathout + os.sep + filename, 'w')
file1.write('time(s)' + '\t' + 'dR/R (*10**(-3))' + '\n')

dvx /= 0.015
dvx *= 10**(3)

for m in range(len(t)):
    file1.write(str(t[m]) +'\t'+ str(dvx[m]) +'\n')  

file1.close()


