# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from scipy.io import savemat
import numpy as np
import matplotlib.pyplot as plt
import glob
import os


def readingextfile(namefile):
    a_file = open(namefile)
    file_contents = a_file.read()
    #print(file_contents)
    contents_split = file_contents.split('; /t')
    a_file.close()
    return contents_split

def subsampling_max(info,sizewindow):
    N_info = len(info)

    meanvalvec = []
    for j in range(0,N_info,sizewindow):
        #window_size = 100
        auxvec = info[j:j+sizewindow]
        meanval = np.max(auxvec)
        #print(meanval)
        meanvalvec.append(meanval)
    return meanvalvec


def truly_string_to_float(arr,offset):
    N = len(arr)

    info = []
    for ii in range(N-1000):
        var = arr[ii]
        if var[0:2] == "/n":
            arr[ii] = var[2:]
           # print(arr[ii])
        info.append(float(arr[ii])+offset)
    return info




# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    directory = r'.'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):

        #output = readingextfile('Result_192.168.67.2_2021-05-20_23-20-14_10.txt')
            print(filename)
            #evaluating the file name
            nameprocess = filename.split('_')
            ip = nameprocess[1]
            date = nameprocess[2]
            time = nameprocess[3]
            nodenumber = nameprocess[4][0:-4]

            print(ip)
            print(date)
            print(time)
            print(nodenumber)


            output = readingextfile(filename)

            arr = np.array(output)

            # getting float format of the information which is originally string.
            offset = 8110
            info = truly_string_to_float(arr,offset)

            # subsampling of info vector with an specific size of window, it will be used to match the
            # sampling rate of the RF information. If we have M elements in the vector plot
            # of latency vector, we should also have M elements in the vector plot of RF vector.
            vector_to_plot = subsampling_max(info,901)

            plt.plot(vector_to_plot)

            #To Plot an extra line with mean value
            mean_val_plotted = np.mean(vector_to_plot)
            plt.plot(np.ones(len(vector_to_plot))*mean_val_plotted)

        
            plt.ylim(ymax=520, ymin=0)
            plt.show()
            print(len(vector_to_plot))

            mdic = {"latency": vector_to_plot}
            savemat("temp.mat",mdic)


