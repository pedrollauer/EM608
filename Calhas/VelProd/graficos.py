import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
from scipy.optimize import curve_fit

# 1. Carregar dados
df = pd.read_csv('r_1.txt', sep='\s+')
t, ax = df['tempo_s'].values, df['ax'].values

# 2. Obter estimativas iniciais via FFT (Chute Inicial)
n, dt = len(t), t[1] - t[0]
yf = fft(ax - np.mean(ax))
xf = fftfreq(n, dt)
idx = np.argmax(np.abs(yf[xf > 0]))
f_guess = xf[xf > 0][idx]
A_guess = 2.0 * np.abs(yf[xf > 0][idx]) / n

# 3. Otimização Não-Linear (Refinamento)
def modelo(t, A, w, phi, offset):
    return A * np.cos(w * t + phi) + offset

# Chute: [Amplitude, Frequência Angular, Fase, Offset]
p0 = [A_guess, 2 * np.pi * f_guess, 0, np.mean(ax)]
popt, _ = curve_fit(modelo, t, ax, p0=p0)

A_ref, w_ref, phi_ref, off_ref = popt

print(f"Parâmetros Refinados:")
print(f"Amplitude (A): {A_ref:.4f} m/s²")
print(f"Freq. Angular (w): {w_ref:.4f} rad/s (f = {w_ref/(2*np.pi):.2f} Hz)")
print(f"Fase (phi): {phi_ref:.4f} rad")
