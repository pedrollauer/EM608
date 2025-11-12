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
E = 210000000000
I = 1

A = m.pi*(r**2)
V = A*h
m = rho*V

w0 = g*m/h
print(f"w0 = {w0}")

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
    m[i] = -w0*f_s(x[i], 0,2)/2 + Ra*f_s(x[i], 0,1)  - w0*h*h/8 + Ra*f_s(x[i], h,1)
    theta[i] = -w0*f_s(x[i], 0,3)/6 + Ra*f_s(x[i], 0,2)/2 -(w0*h*h/8)*x[i] #+ Ra*f_s(x[i], h,2)/2
    #delta[i] = (1/E*I)*(-w0*f_s(x[i], 0,4)/24 + Ra*f_s(x[i], 0,3)/6 + Ra*f_s(x[i], h,3)/6 + -(w0*h*h/8)*x[i]*x[i]/2)

    R_A = Ra
    M_A = w0*h*h/12

    m[i] = M_A*f_s(x[i], 0, 0) + R_A*f_s(x[i], 0, 1) - (w0/2)*f_s(x[i], 0, 2) + (w0/2)*f_s(x[i], h, 2)

    theta[i] = (1/(E*I)) * ( M_A*f_s(x[i], 0, 1) + (R_A/2)*f_s(x[i], 0, 2) - (w0/6)*f_s(x[i], 0, 3) + (w0/6)*f_s(x[i], h, 3) )

    delta[i] = (1/(E*I)) * ( (M_A/2)*f_s(x[i], 0, 2) + (R_A/6)*f_s(x[i], 0, 3) - (w0/24)*f_s(x[i], 0, 4) + (w0/24)*f_s(x[i], h, 4) )
    delta[i] = (1/(E*I)) * ( (M_A/2)*f_s(x[i], 0, 2) + (R_A/6)*f_s(x[i], 0, 3) - (w0/24)*f_s(x[i], 0, 4) + (w0/24)*f_s(x[i], h, 4) + (R_A/6)*f_s(x[i], h, 3) )

## CC

print(f"C1={C1}")
print(f"W0={w0}")
print(f"Ra = {Ra}")
plt.plot(x,delta,label = "Força cortante")
plt.legend()
plt.show()
