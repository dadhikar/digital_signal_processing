import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
input_dir= "sample"
output_dir = "output"
filelist = os.listdir(input_dir)
filecount = 0
for filename in filelist:
    #filecount += 1
    if filename.endswith('.itx'):            
        with open(input_dir + "/" + filename, "r") as f1:
            readlines = f1.read()
            split_readlines = readlines.split("\n")
            file_to_write = open(output_dir + "/"+'Vt'+str(1)+'.txt', 'w')
            for eachline in range(len(split_readlines)):
                if ((eachline < 3) or eachline > (len(split_readlines) - 9)):
                    continue
                else:
                    split_eachline = split_readlines[eachline].split("\t")
                    time = split_eachline[0]
                    Vx = split_eachline[1]
                    Vy = split_eachline[2]
                    finalstring = time + "\t" + Vx + "\t" + Vy
                    file_to_write.write(finalstring + "\n")
        file_to_write.close()
                    #sys.exit(-1) 
                    
                    
#reading time, vx and vy from the file 
# time, vx, vy = np.loadtxt(path_text+os.sep+file_to_read, skiprows=1,usecols = [0,1,2], unpack=True)

# Remove any trend present on  vx and vy fluctuations.
#vx = signal.detrend(vx, axis=-1, type='linear', bp=0)
#vy = signal.detrend(vy, axis=-1, type='linear', bp=0)