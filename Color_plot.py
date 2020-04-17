"""
Created on Wed Feb 14 16:18:47 2018
@author: Dasharath Adhikari
"""
import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator

"""This block of code converts '.itx' files in "inputdir"
to '.txt' files and keep them in the folder name 'output_file' """

inputdir = 'CuIr2S4_IV'
outputdir = 'output_file'
filelist = os.listdir(inputdir)
linecount = 0
for file in filelist:
    if file.endswith('.itx'):
        #sys.exit(-1)
        linecount += 1
        with open(inputdir + '/' + file, 'r') as myfile:
            readlines = myfile.read()
            split_lines = readlines.split('\n')
            FileToWrite = open(outputdir +'/'+'IV'+ str(linecount-1)+'.txt', 'w')
            for line in range(len(split_lines)):
                if((line<3)or (line> len(split_lines)-7)):
                   continue
                else:
                    each_data = split_lines[line].split('\t')
                    time = each_data[0]
                    temperature = each_data[1]
                    voltage = each_data[2]
                    current = each_data[3]
                    final_string = time+'\t'+temperature+'\t'+voltage+'\t'+current
                    FileToWrite.write(final_string + '\n')
                    
            FileToWrite.close()
""" Now matrix of (filenumber, len(current_values)) will be created """

current_matrix = np.zeros((88,2501))
#print(current_matrix.shape)
#sys.exit(-1)
for file_count in range(88):
    #print(file_count)
    #sys.exit(-1)
    filename = 'IV'+str(file_count)+'.txt'
    #print(filename)
    #sys.exit(-1)
    current_array = []
    with open(outputdir + os.sep + filename, 'r') as f:
        datas = f.readlines()
        for values in datas:
            each_value = values.split("\t")
            current_value = each_value[3]
            current_array.append(current_value)
        if file_count%2 != 0:
            current_array.reverse()
            current_matrix[file_count] = (current_array)
        else:
            current_matrix[file_count] = np.asarray(current_array)
            
#print(current_matrix.shape) 
#print(current_matrix[3]) 
Tem = np.linspace(200,243, 44, endpoint=True)
Temperature = np.repeat(Tem,2)
Voltage = np.linspace(0,5,2501, endpoint=True)
X, Y = np.meshgrid(Voltage, Temperature)
#print(Y.shape)
#levels = MaxNLocator(nbins=15).tick_values(current_matrix.min(), current_matrix.max())
cmap = plt.get_cmap('inferno')
#norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
fig, ax = plt.subplots(figsize=(8,8))  
p = ax.pcolor(X, Y, current_matrix, cmap=cmap)
ax.axis('tight')
ax.set_ylabel(r"$Temperature(K)$", fontsize=15)
ax.set_xlabel(r"$Voltage(V)$", fontsize=15)
cb = fig.colorbar(p, ax=ax)
cb.set_label(r'$Current(A)$', fontsize=15)

           
            
            
            
        
        
 
           
                    
                    
                    
                    
                    
                    
                        
            
        
        