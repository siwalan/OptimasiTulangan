"""
@author: gho
"""

import math
import numpy as np
from pyswarm import pso

# Masukan Ukuran Tulangan (1 lonjor standard)
Ls = 12.19;
unit_weight = 52;

# Masukan Ukuran Tulangan yang ingin dipotongkan
# Misal, Tulangan dengan panjang 3 meter, 5 meter, dan 7 meter
# L = [ 7, 5, 3]
L = np.array([5.79,4.72,4.57,3.36,3.05,2.59]);

# Masukan Jumlah Tulangan yang ingin dipotongkan
# DENGAN urutan yang sama dengan yang di atas
# D = [ 1 2 30] = 1 Tulangan 7 Meter, 2 Tulangan 5 meter dan 30 tulangan 3 meter
D = np.array([4,4,4,4,4,4]);


# Menghasilkan Matrix Kosong Untuk Membuat Pattern
A = np.zeros((1,L.shape[0]));
             
i = 0;

for j in range (0,L.shape[0]):
    if j== 0:
        A[i,j] = min(math.floor(Ls/L[j]),D[j])
        s = np.multiply(A[i,j],L[j]);
    elif j>1:
        A[i,j] = min(math.floor((Ls-s)/L[j]),D[j])
        s = s+np.multiply(A[i,j],L[j]);

for j in range (0,(L.shape[0])):
    if A[i,j] > 0:
        k = j+1

i = 1

while k>0:
    A = np.append(A, np.zeros((1,L.shape[0])), axis = 0)
    s=0;
    k = k-1
    for j in range (0,L.shape[0]):
        if j<k:
            A[i,j]=A[i-1,j]
            s = s+np.multiply(A[i,j],L[j]);
        elif j==k:
            A[i,j]=A[i-1,j]-1;
            s = s+np.multiply(A[i,j],L[j]);
        elif j>k:
            A[i,j] = min(math.floor((Ls-s)/L[j]),D[j])
            s = s+np.multiply(A[i,j],L[j]);
    k=0;
    for j in range (0,(L.shape[0])):
        if A[i,j] > 0:
            k = j+1
    
    i = i+1
    
A = np.resize(A, ((A.shape[0]-1),A.shape[1]))

# Matrix A mengandung Pattern yang dapat dipakai    
#
#<---------------------------------------------->
#     Mulai Memasuki Bagian Optimasi


def DSP(x):
    x = np.round(x)
    x= x.reshape(A.shape[0],1)
    cut = np.sum(x*A,axis = 0)
    C = np.sum(A*L*x,axis=1)
    if np.all(np.greater_equal(cut,D)):
        f = np.sum(Ls*x) -  np.sum(C)
        f = f * unit_weight
        print(f)
    else:
        f = 10^9999
    return f

ub= A.shape[0] * [4]
lb= A.shape[0] * [0]

xopt, fopt = pso(DSP, lb, ub,omega=0.9, phip=0.9, phig=0.9,  swarmsize=4000, maxiter=1000,minstep=5e-2,
   minfunc=1e-15)

