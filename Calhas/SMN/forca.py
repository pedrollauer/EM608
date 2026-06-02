import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# ==========================
# Parâmetros do problema
# ==========================
m = 0.23424       # massa (kg)
g = 9.81      # gravidade (m/s²)
C = 940*np.sqrt(2)/10**6      # constante
w = 2*np.pi*(60)      # frequência angular (rad/s)

# ==========================
# Sistema de EDOs
# y[0] = x
# y[1] = dx/dt
# ==========================
def sistema(t, y):
    x, v = y

    # Evita divisão por zero
    if abs(x) < 1e-6:
        x = np.sign(x)*1e-6 if x != 0 else 1e-6
    fd= (C/m) * np.sin(w*t) / (x**2)
    if g- fd>0:
        dxdt=0
        dvdt=0
    else:
        dxdt = v
        dvdt = g -fd

    return [dxdt, dvdt]
result=50
x0=30
# ==========================
# Condições iniciais
# ==========================
for i in range (0,10000) :
        
    x0 = 1 - 0.0001*i    # posição inicial (m)
    v0 = 0.0      # velocidade inicial (m/s)

    # ==========================
    # Intervalo de integração
    # ==========================
    t0 = 0
    tf = 1

    t_eval = np.linspace(t0, tf, 50000)

    # ==========================
    # Solução
    # ==========================
    sol = solve_ivp(
        sistema,
        (t0, tf),
        [x0, v0],
        t_eval=t_eval,
        method='RK45'
    )

    result=sol.y[0][len(sol.y[0])-1]
    

    if result<=0:
        break

print(result)
print(x0)

print(f"CONSTANTE: {C}")

# ==========================
# Gráficos
# ==========================
plt.figure(figsize=(10,5))
plt.plot(sol.t, sol.y[0])
plt.xlabel('Tempo (s)')
plt.ylabel('Posição x (m)')
plt.title('Solução da Equação Diferencial')
plt.grid(True)
plt.show()

plt.figure(figsize=(10,5))
plt.plot(sol.t, sol.y[1])
plt.xlabel('Tempo (s)')
plt.ylabel('Velocidade (m/s)')
plt.title('Velocidade')
plt.grid(True)
plt.show()
