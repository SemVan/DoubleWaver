import csv
import os

REPORTS_PATH = "./Reports/"

def write_report(file_name, data):
    full_path = REPORTS_PATH + file_name
    with open(full_path, 'w') as file:
        writer = csv.writer(file, delimiter = ',')
        for key in data:
            row = [key, str(data[key])]
            writer.writerow(row)
    return


def read_report(file_name):

    data = 0
    return data
