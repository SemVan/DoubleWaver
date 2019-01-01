from file_saver import *
from math_script import *
from reporter import *
import os

SIGNALS_PATH = "./Signals"

for folder_name in os.listdir(SIGNALS_PATH):
    print(folder_name)
    full_path = SIGNALS_PATH + '/' + folder_name
    experiment_data = dict()
    for file_name in os.listdir(full_path):
        full_name = full_path + '/' + file_name
        print(full_name)
        exp_name, p1, p2 = parse_file_name(file_name)
        sig1, sig2 = read_file(full_name)
        plot_signals(sig1, sig2)
        shift = get_phase_shift(sig1, sig2)
        experiment_data[p2] = shift
    report_file_name = exp_name+".csv"
    write_report(report_file_name, experiment_data)
