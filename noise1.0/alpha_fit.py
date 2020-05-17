"""Created on Wed Mar 27 19:58:41 2019 @author: dasharath"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import seaborn as sb

#b.set(context='notebook', style='ticks', palette='bright', font='sans-serif', font_scale = 1.5,
#      color_codes =True, rc=None)
#b.color_palette(palette=None, n_colors=None, desat=None)

path = "/home/dadhikar/Desktop/__CuIr2S4_V2__/Thermal noise/psd/"

print('Enter the name of the psd file: ')
print('-'*25)
psd_file_name = input()
print('-'*25)

f1, S1 = np.loadtxt(path + os.sep+ psd_file_name, skiprows = 1, usecols = [0,4], unpack =True)

list_f = []
for i in range(len(f1)):
    if f1[i] > 1.0:
        continue
    else:
        list_f.append(f1[i])

f1 = np.asarray(list_f)
S1 = S1[0:len(f1)]

S = np.log10(S1)
f = np.log10(f1)
slope, intercept, r_value, p_value, std_err = stats.linregress(f, S)

print("."*30)
print(f"The intercept: {intercept} and the slope: {slope}")
print("."*30)

S_fit = slope* f + intercept


fig, ax = plt.subplots(1,1, figsize=(5, 5), dpi= 200)
ax.plot(f, S, "bo", label = "PSD")
ax.plot(f, S_fit, color='r', label = f"Linear fit, slope ={round(slope, 3)}")
ax.set_xlabel(r"$\log_{10}(f [Hz])$",  fontsize=10)
ax.set_ylabel(r"$\log_{10}(S)$", fontsize=10)
#ax.set_xlim(f.min(), f.max())
#ax.set_ylim(10e-14, 10e-1)
#ax.set_title("")
ax.legend(loc=2)
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True
plt.show()

FileToWrite = open(path + os.sep + 'psd_fit.txt', 'w')
FileToWrite.write('f' +'\t'+ 'S_n' +'\t'+ 'S_fit' + '\n')
for i in range(len(f)):
    FileToWrite.write(str(10**(f[i])) +'\t'+ str(10**(S[i])) +'\t'+ str(10**(S_fit[i])) + '\n')
    
FileToWrite.close()    
