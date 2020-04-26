import os
import numpy as np
import sys

#input_dir = "Insert here"
#output_dir = "Insert here"
input_dir= "/Users/dadhikar/Downloads/Experiment_104"
output_dir = "/Users/dadhikar/Downloads/Experiment_104/Thermal_noise_D2"
filelist = sorted(os.listdir(input_dir))
#print(filelist)
#sys.exit()
filecount = 5611
for filename in filelist:
    if filename.endswith('.itx'):
        filecount += 1            
        with open(input_dir + os.sep + filename, "r") as f1:
            readlines = f1.read()
            split_readlines = readlines.split("\n")
            file_to_write = open(output_dir + "/"+'VT'+str(filecount)+'.txt', 'w')
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