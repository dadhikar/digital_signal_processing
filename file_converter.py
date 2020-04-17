"""Created on Thu May 17 14:15:43 2018 @author: Dasharath Adhikari"""

import os
import sys

# check rootpath
# name of the file to create

def itx_to_txt_converter(raw_data_path, text_data_path):
    """
    raw_data_path is the location fo raw data from the measurement
    text_data_path is the file location for the output text data
    This function converts igor file (.itx file) form noise measurement
    into text file. 
    The igor files are in the path_raw directory and the converted text file will
    be stored in the path_txt directory
    """
    # creates list from the sorted files in the path_raw directory
    filelist = sorted(os.listdir(raw_data_path))    
    linecount = 0
    for file in filelist:
        if file.endswith('.itx'):
            #sys.exit(-1)
            linecount += 1
            print('-'*20)
            print('File number: ', linecount)
            print('-'*20)
            with open(raw_data_path + os.sep + file, 'r', encoding='ISO-8859-1') as myfile:
                readlines = myfile.read()
                split_lines = readlines.split('\n')
                FileToWrite = open(text_data_path + os.sep +'VT'+ str(linecount)+'.txt', 'w')
                FileToWrite.write('time(s)' +'\t'+ 'v_x (V)' +'\t'+ 'v_y (V)' +'\n')
                for line in range(len(split_lines)):
                    if((line<3)or (line> len(split_lines)-9)):
                        continue
                        # print("Comment lines are encountered")
                    else:
                        each_data = split_lines[line].split('\t')
                        time = each_data[0]
                        v_x  = each_data[1]
                        v_y  = each_data[2]
                        final_string = time +'\t'+ v_x +'\t'+ v_y
                        FileToWrite.write(final_string + '\n')                    
                FileToWrite.close()