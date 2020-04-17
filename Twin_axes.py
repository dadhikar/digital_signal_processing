"""Need some work"""
import os
import matplotlib.pyplot as plt
import numpy as np
file_dir = 'output'
file = os.listdir(file_dir)
fig, ax1 = plt.subplots(figsize=(5, 5), dpi=100, facecolor='#f1f1f1', 
                 edgecolor='none', frameon=False)
time = np.loadtxt(file_dir + os.sep + file, usecols=0)
Vx = np.loadtxt('Vt1.txt', usecols=1)
Vy = np.loadtxt('Vt1.txt', usecols=2)
V = Vx - Vy
ax1.plot(time, V, color='red', label='Signal')
ax1.set_xlabel('Time(s)',fontsize=16)
ax1.set_ylabel('Signal+background($V$)', fontsize=16, )
ax1.legend(loc= 1)
ax1.xaxis.set_ticks_position('both')
ax1.yaxis.set_ticks_position('both')
#ax2 = ax1.twinx()
#ax2.plot(time, Vy, color='red', lw=2, ls=':', label='Background')
#ax2.set_ylabel('Background($V$)', fontsize=16)
#ax2.legend()
plt.show()
"""