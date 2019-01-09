import csv
import os
import numpy as np

REPORTS_PATH = "./Reports/"
MATRICES_PATH = "./Matrices"

def write_report(file_name, data):
    full_path = REPORTS_PATH + file_name
    with open(full_path, 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        keys = []
        for key in data:
            keys.append(int(key))
        keys = sorted(keys)
        for key in keys:
            for num in data[str(key)]:
                row = [str(key), num, str(data[str(key)][num])]
                writer.writerow(row)
    return


def write_matrices(file_name, matrices, device_shift):
    full_path = MATRICES_PATH + '/' + file_name
    with open(full_path, 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(device_shift)
        for mat in matrices:
            for row in mat:
                writer.writerow(row)
    return


def read_matrices(file_name):
    full_path = MATRICES_PATH + '/' + file_name
    full_data = []
    with open(full_path, 'r') as file:
        reader = csv.reader(file, delimiter = ',')

        for row in reader:
            new_row = [float(x) for x in row]
            full_data.append(new_row)

    device_shift = np.asarray(full_data[0])
    matrices = np.zeros(shape = (3, 8, 7))
    for i in range(1, len(full_data)):
        mat_num = (i-1)//8
        row_num = (i-1)%8
        matrices[mat_num][row_num] = np.asarray(full_data[i])
    return matrices, device_shift
