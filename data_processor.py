from file_saver import *
from math_script import *
from reporter import *
import os
from scipy.signal import savgol_filter
import numpy as np

SIGNALS_PATH = "./Signals/Exper"

float_formatter = lambda x: "%.4f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

for folder_name in os.listdir(SIGNALS_PATH):
    #print(folder_name)
    print()
    full_path = SIGNALS_PATH + '/' + folder_name
    experiment_data = dict()
    full_matrix = np.zeros(shape = (3, 8, 7))

    for file_name in os.listdir(full_path):
        full_name = full_path + '/' + file_name
        # print(full_name)

        exp_name, p1, p2, num = parse_file_name(file_name)
        sig1, sig2 = read_file(full_name)
        sig1, sig2, shift = full_signals_procedure(sig1, sig2)
        # plot_signals(sig1, sig2, 0)

        p = int(p2)-1

        # if (p>28):
        #     p = p-7

        row = p//7
        col = p%7
        print(int(num), row, col)

        if abs(shift)>=0.1:
            shift = 0

        if p>=0:
            full_matrix[int(num)-1, row, col] = shift

        if p2 in experiment_data:
            experiment_data[p2][num] = shift
        else:
            experiment_data[p2] = dict()
            experiment_data[p2][num] = shift

    print(full_matrix)
    print()
    shift_matrix_procedure(full_matrix)
    report_file_name = exp_name+".csv"
    write_report(report_file_name, experiment_data)
