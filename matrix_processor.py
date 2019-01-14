from reporter import *
from math_script import *
import numpy as np
import os
import matplotlib.backends.backend_pdf
from matplotlib import pyplot as plt



figures = []
rows = []
cols = []
for file_name in os.listdir(MATRICES_PATH):
    full_path = MATRICES_PATH + '/' + file_name
    print(file_name)
    mat, inst = read_matrices(file_name)
    print(inst)
    row, col = shift_matrix_procedure(mat, inst, file_name )
    rows.append(row)
    cols.append(col)
rows = np.asarray(rows)
cols = np.asarray(cols)


plt.subplot(2,1,1)
plt.grid()
for col in cols:
    new_col = col-np.mean(col)
    plt.plot(range(len(col)), new_col)


plt.subplot(2,1,2)
for row in rows:
    new_row = row-np.mean(row)
    plt.plot(range(len(row)), new_row)

plt.grid()
plt.show()


m_r = np.mean(rows, axis=0)
m_c = np.mean(cols, axis=1)

std_r = np.std(rows, axis=0)
std_c = np.std(cols, axis=1)

k = 3
l_r = m_r + k*np.square(std_r)
u_r = m_r - k*np.square(std_r)

l_c = m_c + k*np.square(std_c)
u_c = m_c - k*np.square(std_c)

plt.subplot(2,1,1)
plt.grid()
plt.plot(range(len(m_r)), m_r)
plt.plot(range(len(m_r)), l_r, linestyle=':', color='red')
plt.plot(range(len(m_r)), u_r, linestyle=':', color='red')

plt.subplot(2,1,2)
plt.grid()
plt.plot(range(len(m_c)), m_c)
plt.plot(range(len(m_c)), l_c, linestyle=':', color='red')
plt.plot(range(len(m_c)), u_c, linestyle=':', color='red')

plt.show()
