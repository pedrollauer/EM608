import math as m
import numpy as np
import matplotlib.pyplot as plt

def f_s(x, L, n):
    if(x < L):
        return 0;
    if n>=1:
        if x > L:
            return float((x-L)**n)
        else :
            return float(0)
    elif n == 0:
        return 1;
    # elif n == -2:
    #     return 0
    # elif n == -1:
    #         return 0
    


g = 9.8
d = 12.7/1000 #mm
r = d/2
rho = 7850
h=1490.48/1000

A = m.pi*(r**2)
V = A*h
m = rho*V

w0 = g*m/h
print(w0)

tamanho_x = 1000

passo = h/tamanho_x

x = np.zeros(tamanho_x)
v = np.zeros(tamanho_x)
m = np.zeros(tamanho_x)
theta = np.zeros(tamanho_x)
delta = np.zeros(tamanho_x)
acumulador = 0


Ra = h*w0/2
### Pontos para o eixo
for i in range(0, tamanho_x):
               acumulador = acumulador + passo
               x[i] = acumulador
a = f_s(0,h,1)
print(f"fs = {a}")

# CC
C1 = (2*Ra - w0*h) 
for i in range(0,tamanho_x):
    v[i] = -w0*f_s(x[i], 0,1) + Ra*f_s(x[i], 0,0) + Ra*f_s(x[i], h,0)
    #v[i] =  Ra*f_s(x[i], 1.5,0) 
    m[i] = -w0*f_s(x[i], 0,2) + Ra*f_s(x[i], 0,1) + Ra*f_s(x[i], h,1)
    theta[i] = w0*f_s(x[i], 0,3) + Ra*f_s(x[i], 0,2) + Ra*f_s(x[i], h,2)
    delta[i] = w0*f_s(x[i], 0,4) + Ra*f_s(x[i], 0,3) + Ra*f_s(x[i], h,3)
    # delta[i] = w0*f_s(x[i], 0,2) + Ra*f_s(x[i], 0,1) + Ra*f_s(x[i], h,1)

## CC


print(f"C1={C1}")
print(f"W0={w0}")
print(f"Ra = {Ra}")
plt.plot(x,m,label = "Momento fletor")
plt.legend()
plt.show()
