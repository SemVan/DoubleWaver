from data_grabber import *
from file_saver import *
import os

work_port = find_port(get_list_of_com_ports())
if work_port == 1:
    exit()
print(work_port.port)
print()

print("Enter series name")
folder_name = input()
folder_name = "./" + folder_name
if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

for point_num in range(1, 57):
    for attempt in range(1, 4):
        fp = 0
        print("First point ", fp)
        sp = point_num
        print("Second point ", sp)
        np = attempt
        print("Number of measurement ", np)
        fileName = folder_name + "/" + folder_name + "_" + fp + "_" + sp + "_" + np + ".txt"

        sig1, sig2 = one_measurement_procedure(work_port)
        write_file(fileName, sig1, sig2)
