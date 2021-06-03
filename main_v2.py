# This is a python script that is doing preprocessing of data gathered from the field
# Autor: Dick Carrillo Melgarejo
# Date: 31/05/2021
# Description:
# ==========
# this script organize the dataset by IP number and Sampling time. Each txt file is plotted
# The plot contains reliability and latency information. Each sampling is representing 1 second of test
#

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
    flag = 0
    for ii in range(len(contents_split)):
      #  print(contents_split[ii][0:2])
       # print(contents_split[ii])
        if (contents_split[ii][0:2] == '/n') and (flag==0):
            index_limiter = ii
            flag=1 #used to not repeat this condition in the second time

            # elimnating the /n signal and save the value
            value = contents_split[ii][2:]
            contents_split[ii] = value
    #Reliability data is until the index_limiter
    reliability_info = contents_split[:index_limiter-1]

    #Latency data is between the index_limiter until the last sample-1.
    latency_info = contents_split[index_limiter:-1]
    a_file.close()
    return reliability_info, latency_info

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
    for ii in range(N):
        var = arr[ii]
        info.append(float(arr[ii])+offset)
    return info

def sorting_filenames_generic(vector_info_tobe_sorted, criteria):
    info = vector_info_tobe_sorted
    size_info = len(info)
    print(size_info)

    new_mapping_vector = []  # The vector output
    vector_features = []
    index_counter= 0
    for ii in range(size_info):

        infobeprocessed = info[ii]
        [ip, date, time, sampling_id] = processingname(infobeprocessed)



        if criteria == 'ip':
            [ipdigit, ipbase] = processingipname(ip)
            vector_features.append(ipdigit)
        elif criteria == 'date':
            [year, month, day] = getting_dataset_date(date)
            year_in_days = 365 * int(year)
            month_in_days = 30 * int(month)
            date_info = year_in_days + month_in_days + int(day)
            #Check that this vector is a integer number, it should be post processed in the next stage
            vector_features.append(date_info)

        elif criteria == 'time':
            [hour, minutes, seconds] = getting_dataset_time(time)
            hour_in_seconds = 3600 * int(hour)
            minutes_in_seconds = 60 * int(minutes)
            time_info = hour_in_seconds + minutes_in_seconds + int(seconds)
            #Check that this vector is a integer number, it should be post processed in the next stage
            vector_features.append(time_info)

        elif criteria == 'sampling':
            print(sampling_id)
            vector_features.append(int(sampling_id))

        else:
            print('Choose other criteria...')
    vector_features_sorted_unique = sorted(set(vector_features))

    #generating new list names
    size_feature_vec = len(vector_features_sorted_unique)


    index_counter_vector = []
    vec_jj = []
    for jj in range(size_feature_vec):

        for ii in range(size_info):

            infobeprocessed = info[ii]
            [ip, date, time, sampling_id] = processingname(infobeprocessed)

            if criteria == 'ip':
                size_outvec = len(new_mapping_vector)
                [ipdigit, ipbase] = processingipname(ip)
                if ipdigit == vector_features_sorted_unique[jj]:
                    #new_name_ip = '192.168.241.'+ip
                    new_mapping_vector.append(infobeprocessed)

            elif criteria == 'date':
                size_outvec = len(new_mapping_vector)
                [year, month, day] = getting_dataset_date(date)
                year_in_days = 365 * int(year)
                month_in_days = 30 * int(month)
                date_info = year_in_days + month_in_days + int(day)
                # Check that this vector is a integer number, it should be post processed in the next stage
                if date_info == vector_features_sorted_unique[jj]:
                    new_mapping_vector.append(infobeprocessed)

            elif criteria == 'time':
                size_outvec = len(new_mapping_vector)
                [hour, minutes, seconds] = getting_dataset_time(time)
                hour_in_seconds = 3600 * int(hour)
                minutes_in_seconds = 60 * int(minutes)
                time_info = hour_in_seconds + minutes_in_seconds + int(seconds)
                # Check that this vector is a integer number, it should be post processed in the next stage
                if time_info == vector_features_sorted_unique[jj]:
                    new_mapping_vector.append(infobeprocessed)

            elif criteria == 'sampling':
                size_outvec = len(new_mapping_vector)
                if int(sampling_id) == vector_features_sorted_unique[jj]:
                    new_mapping_vector.append(infobeprocessed)

            else:
                print('Choose other criteria...')
        index_counter_vector.append(size_outvec)
    return new_mapping_vector, index_counter_vector, size_feature_vec, vector_features_sorted_unique

def getting_dataset_date(date):
    date_vector = date.split('-')
    year = date_vector[0]
    month = date_vector[1]
    day = date_vector[2]
    return year, month, day

def getting_dataset_time(time):
    data_vector = time.split('-')
    hour = data_vector[0]
    minutes = data_vector[1]
    seconds = data_vector[2]
    return hour, minutes, seconds


def processingname(filename):

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

    return ip, date, time, nodenumber

def processingipname(varname):
    print(varname)
    # evaluating the file name
    print(varname)
    nameprocess = varname.split('.')
    #We know that all nodes are in the same network, so the unique difference is the last number
    ipdigit = nameprocess[3]
    ipbase = nameprocess[0]+'.'+nameprocess[1]+'.'+nameprocess[2]
  #  print(ipdigit, ipbase)

    return ipdigit,ipbase

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    directory = r'./field_info/Result_data_2'
    vector_info_tobe_sorted = os.listdir(directory)
    print(type(vector_info_tobe_sorted))

    # Clustering the dataset based on the IP address
    criteria = 'ip'
    [info_sorted, index_groups, size_feature_vec, vector_features_sorted_unique] = \
        sorting_filenames_generic(vector_info_tobe_sorted, criteria)


    # generating new vectors per IP number using an automatic iteration
    # The vectors name starts with 'info_only_ip_'
    N_groups = len(index_groups)
    base_name = 'info_only_ip_'
    for ii in range(N_groups):
        vec_name = base_name+vector_features_sorted_unique[ii]
        if ii == 0:
            exec_string = vec_name + '= info_sorted[:index_groups[0]]'
        elif ii == N_groups-1:
            exec_string = vec_name + '= info_sorted[index_groups['+str(ii-1)+']+1:]'
        else:
            exec_string = vec_name + '= info_sorted[index_groups['+str(ii-1)+']+1:index_groups['+str(ii)+']]'
        print(exec_string)
        exec(exec_string)

    #info_solo_ip_11 = info_sorted[:index_groups[0]]
    #info_solo_ip_12 = info_sorted[index_groups[0]+1:index_groups[1]]
    #info_solo_ip_14 = info_sorted[index_groups[1]+1:]

    # Since this point, we can process which was clustered . For example
    info_sorted_clustered = info_only_ip_11
    criteria2 = 'sampling'

    [info_sorted_x, index_groups_x, size_feature_vec_x, vector_features_sorted_unique_x] = \
        sorting_filenames_generic(info_sorted_clustered, criteria2)
   # info_sorted_x
  #  for filename in os.listdir(directory):
    for filename in info_sorted_x:
        if filename.endswith(".txt"):

            [ip, date, time, sampling] = processingname(filename)

            dir_filename = directory+'/'+filename
            [reliability_info, latency_info] = readingextfile(dir_filename)

            arr_reliability = np.array(reliability_info)

            # getting float format of the information which is originally string.
            offset = 0
            info = truly_string_to_float(arr_reliability,offset)

            # subsampling of info vector with an specific size of window, it will be used to match the
            # sampling rate of the RF information. If we have M elements in the vector plot
            # of latency vector, we should also have M elements in the vector plot of RF vector.
            #vector_to_plot = subsampling_max(info,901)
            vector_to_plot = subsampling_max(info, 1)

            plt.plot(vector_to_plot)

            #To Plot an extra line with mean value
            mean_val_plotted = np.mean(vector_to_plot)
            plt.plot(np.ones(len(vector_to_plot))*mean_val_plotted)
            plt.title('Reliability:'+ip+'|'+date+'|'+time+'|'+sampling)

        
          #  plt.ylim(ymax=520, ymin=0)
            plt.show()
            print(len(vector_to_plot))

            namefigure = dir_filename[:-4]+'_reliability.png'
            plt.savefig(namefigure)

            mdic = {"reliability": vector_to_plot}
            savemat("temp_reliability.mat",mdic)

        arr_latency = np.array(latency_info)

        # getting float format of the information which is originally string.
        offset = 0
        info = truly_string_to_float(arr_latency, offset)

        # subsampling of info vector with an specific size of window, it will be used to match the
        # sampling rate of the RF information. If we have M elements in the vector plot
        # of latency vector, we should also have M elements in the vector plot of RF vector.
        # vector_to_plot = subsampling_max(info,901)
        subsamplingrate = int(1000/int(sampling))
        #subsamplingrate =1
        vector_to_plot = subsampling_max(info, subsamplingrate)

        plt.plot(vector_to_plot)

        # To Plot an extra line with mean value
        mean_val_plotted = np.mean(vector_to_plot)
        plt.plot(np.ones(len(vector_to_plot)) * mean_val_plotted)
        plt.title('Latency:'+ip + '|' + date + '|' + time + '|' + sampling)

        #  plt.ylim(ymax=520, ymin=0)
        plt.show()
        print(len(vector_to_plot))

        namefigure = dir_filename[:-4] + '_latency.png'
        plt.savefig(namefigure)

        mdic = {"latency": vector_to_plot}
        savemat("temp_latency.mat", mdic)


