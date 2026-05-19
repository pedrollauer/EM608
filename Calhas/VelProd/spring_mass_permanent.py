import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do sistema
m = 1.0       # Massa (kg)
k = 10.0      # Constante da mola (N/m)
c = 0.5       # Coeficiente de amortecimento (N.s/m)
F0 = 1.0      # Amplitude da força (N)
w = 2.0       # Frequência da força (rad/s)

# Cálculo Analítico da Resposta Permanente
# Amplitude (X): F0 / sqrt((k - m*w**2)**2 + (c*w)**2)
# Fase (phi): arctan2(c*w, k - m*w**2)

denominator = np.sqrt((k - m * w**2)**2 + (c * w)**2)
X_amplitude = F0 / denominator
phi = np.arctan2(c * w, k - m * w**2)

# Tempo de simulação (mostrando 4 ciclos para clareza)
period = 2 * np.pi / w
t = np.linspace(0, 4 * period, 1000)

# Funções do Regime Permanente
# Nota: Usamos sin(w*t - phi) para manter a coerência com a força F0*sin(w*t)
x_perm = X_amplitude * np.sin(w * t - phi)
v_perm = X_amplitude * w * np.cos(w * t - phi)
a_perm = -X_amplitude * (w**2) * np.sin(w * t - phi)

# Plotagem
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

axs[0].plot(t, x_perm, 'b', label='Deslocamento Permanente')
axs[0].set_ylabel('Posição [m]')
axs[0].grid(True)
axs[0].legend()
axs[0].set_title('Resposta em Regime Permanente (Steady-State)')

axs[1].plot(t, v_perm, 'g', label='Velocidade Permanente')
axs[1].set_ylabel('Velocidade [m/s]')
axs[1].grid(True)
axs[1].legend()

axs[2].plot(t, a_perm, 'r', label='Aceleração Permanente')
axs[2].set_ylabel('Aceleração [m/s²]')
axs[2].set_xlabel('Tempo [s]')
axs[2].grid(True)
axs[2].legend()

plt.tight_layout()
plt.show()
