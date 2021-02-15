import numpy as np
from mesh import Mesh
from FVMO import compute_matrix as compute_matrix_o
from FVML import compute_matrix, compute_vector
from differentiation import gradient, divergence
import sympy as sym
import math
import matplotlib.pyplot as plt
import random
from scipy.sparse import csr_matrix,lil_matrix
from scipy.sparse.linalg import spsolve
import time as time


K = np.array([[1,0],[0,1]])
transform = np.array([[1,0],[0.1,1]])
x = sym.Symbol('x')
y = sym.Symbol('y')
u_fabric = sym.cos(y*math.pi)*sym.cosh(x*math.pi)


#u_fabric = (x*y*(1-x)*(1-y))
source = -divergence(gradient(u_fabric,[x,y]),[x,y],permability_tensor=K)
print(source)
source = sym.lambdify([x,y],source)
u_lam = sym.lambdify([x,y],u_fabric)
nx = 8
ny = 8

#T = lambda x,y: (0.9*y+0.1)*math.sqrt(x) + (0.9-0.9*y)*x**2
T = lambda x,y: x + 0.3*y



def random_perturbation(h):
    return lambda x,y: random.uniform(0,h)*random.choice([-1,1]) + x + 0.32*y

# mesh = Mesh(8,8,random_perturbation(0.5/(8)))
mesh = Mesh(nx,ny,T)
mesh.plot()



A,fx,fy = compute_matrix(mesh,K=np.array([[1,0],[0,1]]))
f = compute_vector(mesh,source,u_lam)

u = np.linalg.solve(A,f)

mesh.plot_vector(u,'pressure')

midpoints = mesh.midpoints
fx_mesh = np.zeros((midpoints.shape[0],midpoints.shape[1]-1))

fx_vec = fx@u
print(fx_vec)

for i in range(midpoints.shape[0]*midpoints.shape[1]-nx+1):
    fx_mesh[mesh.vecToMesh(i)] = fx_vec[i]

print(fx_mesh)
plt.contourf(midpoints[:,1:,0,0],midpoints[:,1:,0,1],fx_mesh,20,)
plt.colorbar()

plt.show()
