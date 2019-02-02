from reporter import *
from math_script import *
import numpy as np
import os
import matplotlib.backends.backend_pdf
from matplotlib import pyplot as plt


float_formatter = lambda x: "%.4f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

figures = []
rows = []
cols = []
sects = []
for file_name in os.listdir(MATRICES_PATH):
    full_path = MATRICES_PATH + '/' + file_name
    print(file_name)
    mat, inst = read_matrices(file_name)
    print(inst)
    row, col, sect = shift_matrix_procedure(mat, inst, file_name )
    rows.append(row)
    cols.append(col)
    sects.append(sect)

rows = np.asarray(rows)
cols = np.asarray(cols)
new_rows = []
new_cols = []

plt.figure()
plt.subplot(3,1,1)
plt.grid()
plt.ylim([-0.05, 0.05])
plt.xlabel("Columm number")
plt.ylabel("Delay, s")
plt.title("a) Horizontal distribution")
for col in cols:
    col = col-np.mean(col)
    new_cols.append(col)
    plt.plot(range(len(col)), col)

plt.subplot(3,1,2)
plt.grid()
plt.ylim([-0.05, 0.05])
plt.xlabel("Row number")
plt.ylabel("Delay, s")
plt.title("b) Vertical distribution")
for row in rows:
    row = row-np.mean(row)
    new_rows.append(row)
    plt.plot(range(len(row)), row)

rows = np.asarray(new_rows)
cols = np.asarray(new_cols)
plt.show()
#plt.subplot(3,1,3)
# plt.grid()
# for sect in sects:
#     sect = sect-np.mean(row)
#     plt.plot(range(len(sect)), sect)
plt.imshow(np.mean(sects, axis=0))
plt.colorbar()
plt.tight_layout()
plt.show()


print("ROWS")
print(rows)
print("COLS")
print(cols)
print()
m_r, l_r, u_r, std_r = distrib_procedure(rows)
print('mann whitney rows')
get_mann_whitney_result(rows)
print('mann whitney cols')
get_mann_whitney_result(cols)
m_c, l_c, u_c, std_c = distrib_procedure(cols)
# m_s, l_s, u_s = distrib_procedure(sects)
k = 3
plt.figure()
plt.subplot(3,1,1)
plt.grid()
plt.xlabel("Номер ряда")
plt.ylabel("Задержка, с")
plt.errorbar(range(len(m_r)), m_r, yerr=k*std_r)
# plt.plot(range(len(m_r)), l_r, linestyle=':', color='red')
# plt.plot(range(len(m_r)), u_r, linestyle=':', color='red')

plt.subplot(3,1,2)
plt.grid()
plt.xlabel("Номер строки")
plt.ylabel("Задержка, с")
plt.errorbar(range(len(m_c)), m_c, yerr=k*std_c)
# plt.plot(range(len(m_c)), l_c, linestyle=':', color='red')
# plt.plot(range(len(m_c)), u_c, linestyle=':', color='red')


plt.subplot(3,1,3)
plt.grid()
ms = np.mean(sects, axis=0)
s = np.std(sects, axis=0)
print(ms)
m_s =(np.reshape(ms, (1,np.product(ms.shape))))
std =(np.reshape(s, (1,np.product(s.shape))))
m_s = m_s[0]
std = std[0]
l_s = m_s + std
u_s = m_s - std
print(std)
plt.plot(range(len(m_s)), m_s)
plt.plot(range(len(m_s)), l_s, linestyle=':', color='red')
plt.plot(range(len(m_s)), u_s, linestyle=':', color='red')


plt.show()
