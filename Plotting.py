import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 6), dpi=50)
time_sec = np.loadtxt('Experiment_200K.txt', usecols=0)
time_sec1 = np.delete(time_sec, np.s_[0:120000])
time_m = (1/60.)*time_sec1
V_x = np.loadtxt('Experiment_200K.txt', usecols=1)
V_xnew = np.delete(V_x, np.s_[0:120000])
V_xav = np.mean(V_xnew)
V_x1 = V_xnew - V_xav
print(len(V_x1))
#print(V_x1)
#V_y = np.loadtxt('Experiment_325K.txt', usecols=2)
#ax.plot(time_m, V_x1, color='blue', lw=2, ls='-', label='$200K$')
#ax.set_xlabel('Time(min)',fontsize=25)
#ax.set_ylabel('$V_{x}(V)$', fontsize=25)
#ax.legend()
#ax.xaxis.set_ticks_position('both')
#ax.yaxis.set_ticks_position('both')
#ax[1].xaxis.set_ticks_position('both')
#ax[1].yaxis.set_ticks_position('both')
#plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
#ax[1].plot(time_m, V_y, color='red', lw=2, ls='-', label='$325$')
#ax[1].set_xlabel('Time(min)',fontsize=14)
#ax[1].set_ylabel('$V_{y}(V)$', fontsize=14)
#ax[1].legend()
#plt.show()

