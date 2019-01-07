import csv
import os

REPORTS_PATH = "./Reports/"

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


def read_report(file_name):

    data = 0
    return data
