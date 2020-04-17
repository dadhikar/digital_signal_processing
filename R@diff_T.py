"""
Created on Thu May 17 14:31:12 2018
@author: dasharath adhikari
"""
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

rootpath = "C:\\Users\\das_d\\Desktop\\SUNY\\PhD\\LAB_WORK\\CuIr2S4\\52118\\output(IVs)\\"
linecount = 0
temperature = 240
for filename in sorted(os.listdir(rootpath)):
    linecount +=1
    if filename.endswith('.txt'):
        voltage,current = np.loadtxt(rootpath + os.sep + 'IV'+str(linecount)+'.txt',
                                           skiprows=2, usecols= (1,2), unpack=True)
        
        if linecount == 1:
            temperature += -10
            label = str(temperature)+'K'
        plt.plot(voltage,current, label=label)
        plt.show()
        plt.legend()

sys.exit(-1)    
fileToWrite = open("Resistance_300 K.txt", "w")
fileToWrite.write("Voltage(V)"+"\t"+"Current(A)"+"\t"+"Resistance")
fileToWrite.write("\n")
for m in range(len(v1)):
    for n in range(len(i1)):
        if (m > 0 and n >0):
            if m == n:
                resistance = v1[m]/i1[n]
                fileToWrite.write(str(v1[m])+"\t"+str(i1[n])+"\t"+str(resistance))
                fileToWrite.write("\n")
fileToWrite.close() 

plt.plot(v1[1:900],i1[1:900], label='230 K')
plt.plot(v2[1:1000],i2[1:1000],label='225 K' )
plt.plot(v3[1:1100],i3[1:1100],label='220 K')
plt.plot(v4[1:1100],i4[1:1100],label='210 K')
plt.plot(v5[1:1100],i5[1:1100],label='200 K')
plt.plot(v5[1:1100],i5[1:1100],label='180 K')

plt.legend(loc=2)

plt.show()
           
#    Resistance = np.asarray(list)
#    f.write(Resistance + "\n")          

#f.close()           
#x = np.loadtxt("Resistance_225 K.txt", skiprows=1, usecols= 1)
#print(len(x))













