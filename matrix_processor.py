from reporter import *
from math_script import *
import numpy as np
import os


for file_name in os.listdir(MATRICES_PATH):
    full_path = MATRICES_PATH + '/' + file_name
    print(file_name)
    mat, inst = read_matrices(file_name)
    print(inst)
    shift_matrix_procedure(mat, inst)
