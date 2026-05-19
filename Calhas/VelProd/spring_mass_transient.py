import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parâmetros do sistema
m = 1.0       # Massa (kg)
k = 10.0      # Constante da mola (N/m)
c = 0.5       # Coeficiente de amortecimento (N.s/m) - Amortecimento subcrítico
F0 = 1.0      # Amplitude da força externa (N)
w = 2.0       # Frequência da força (rad/s)

# Equação diferencial: transforma 2ª ordem em um sistema de duas de 1ª ordem
# y[0] = posição (x), y[1] = velocidade (v)
def system_dynamics(y, t, m, c, k, F0, w):
    x, v = y
    accel = (F0 * np.sin(w * t) - c * v - k * x) / m
    return [v, accel]

# Condições iniciais: partindo do repouso
y0 = [0.0, 0.0]

# Tempo de simulação (foco no transiente inicial)
t = np.linspace(0, 20, 1000)

# Solução numérica
sol = odeint(system_dynamics, y0, t, args=(m, c, k, F0, w))

x = sol[:, 0]
v = sol[:, 1]
# Cálculo da aceleração para o plot
a = (F0 * np.sin(w * t) - c * v - k * x) / m

# Plotagem
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

axs[0].plot(t, x, 'b', label='Deslocamento (x)')
axs[0].set_ylabel('Posição [m]')
axs[0].grid(True)
axs[0].legend()
axs[0].set_title('Resposta Transiente: Sistema Massa-Mola Forçado')

axs[1].plot(t, v, 'g', label='Velocidade (v)')
axs[1].set_ylabel('Velocidade [m/s]')
axs[1].grid(True)
axs[1].legend()

axs[2].plot(t, a, 'r', label='Aceleração (a)')
axs[2].set_ylabel('Aceleração [m/s²]')
axs[2].set_xlabel('Tempo [s]')
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()
