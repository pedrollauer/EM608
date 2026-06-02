import numpy as np
from scipy.fft import fft, fftfreq
from scipy.signal import correlate, correlation_lags
from scipy.interpolate import CubicSpline
import vel_atr as va
import math as m
import matplotlib.pyplot as plt



def plot_integral(A, B, a, b, f_hz):

    w = 2 * np.pi * f_hz
    

    T = 1 / f_hz
    t = np.linspace(0, 3 * T, 1000)
    

    y1_orig = A * np.cos(w * t + a)
    y2_orig = B * np.cos(w * t + b)
    

    y1_int = (A / w) * np.sin(w * t + a)
    y2_int = (B / w) * np.sin(w * t + b)
    

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    

    ax1.plot(t, y1_orig, color='blue', linewidth=2, label=f'A: {A}*cos(wt + {a:.2f})')
    ax1.plot(t, y2_orig, color='orange', linewidth=2, label=f'B: {B}*cos(wt + {b:.2f})')
    ax1.set_title(f'Original Signals vs. Integrals at {f_hz} Hz', fontsize=14)
    ax1.set_ylabel('Amplitude (Original)', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=9)
    

    ax2.plot(t, y1_int, color='navy', linestyle='--', linewidth=2, label='Integral of A')
    ax2.plot(t, y2_int, color='chocolate', linestyle='--', linewidth=2, label='Integral of B')
    ax2.set_xlabel('Time (seconds)', fontsize=12)
    ax2.set_ylabel('Amplitude (Integral)', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='upper right', fontsize=9)
    
    plt.tight_layout()
    plt.show()


def plot_cosine_and_integral(A, a, f_hz):
    w = 2 * np.pi * f_hz
    
    T = 1 / f_hz
    t = np.linspace(0, 3 * T, 1000)
    
    y_orig = A * np.cos(w * t + a)
    y_int  = (A / w) * np.sin(w * t + a)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    ax1.plot(t, y_orig, color='blue', linewidth=2, label='Original')
    ax1.set_title(f'Original Signal vs. Its Integral ({f_hz} Hz)', fontsize=14)
    ax1.set_ylabel('Amplitude (Original)', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right')
    
    ax2.plot(t, y_int, color='crimson', linewidth=2, label='Integral')
    ax2.set_xlabel('Time (seconds)', fontsize=12)
    ax2.set_ylabel('Amplitude (Integral)', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

def plot_compare2(ax,ay,t):

    fig, ax1 = plt.subplots()
    
    ax1.plot(t, ax, color='blue', linewidth=2, label='X')
    ax1.plot(t, ay, color='orange', linewidth=2, label='Y')

    ax1.set_title(f'Exp vs Trat', fontsize=14)
    ax1.set_ylabel('Amplitude (Original)', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right')
    
    plt.xlim(5, 5.1)
    plt.show()

def plot_compare(A,a,f,sinal, t):
    w = 2 * np.pi * f
    
    ax = []

    for i in range(0,len(t)):
        dx = A*m.cos(w*t[i]+a)
        ax.append(dx)

    fig, ax1 = plt.subplots()
    
    ax1.plot(t, sinal, color='blue', linewidth=2, label='Experimental')
    ax1.plot(t, ax, color='orange', linewidth=2, label='Experimental')

    ax1.set_title(f'Exp vs Trat', fontsize=14)
    ax1.set_ylabel('Amplitude (Original)', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right')
    
    plt.xlim(10, 10.1)
    plt.show()

def plot_cosine_signals(A, B, a, b, f_hz):
    # 1. Calculate angular frequency (w = 2 * pi * f)
    w = 2 * np.pi * f_hz
    
    # 2. Define time vector (T = 1/f is the period; plot 3 periods for clarity)
    T = 1 / f_hz
    t = np.linspace(0, 3 * T, 1000)
    
    # 3. Calculate signals
    y1 = A * np.cos(w * t + a)
    y2 = B * np.cos(w * t + b)
    
    # 4. Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(t, y1, label=f'{A} * cos(ωt + {a:.4f})', color='blue', linewidth=2)
    plt.plot(t, y2, label=f'{B} * cos(ωt + {b:.4f})', color='orange', linewidth=2)
    
    # Formatting the plot
    plt.title(f'Cosine Signals Comparison at {f_hz} Hz', fontsize=14)
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Amplitude', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper right', fontsize=10)
    
    # Show the plot
    plt.tight_layout()
    plt.show()

def freq(ax,t):

    ddx0 = -1
    f = []

    for i in range(0, len(t) - 1):
        ddx = ax[i]*ax[i+1]

        if ddx < 0 and ddx0 == -1:
            ddx0 = i
            continue

        if ddx < 0 and ddx0 !=-1:
            t_2 = t[i] - (ax[i]/(ax[i+1] - ax[i]))*(t[i+1] - t[i])
            t_1 = t[ddx0] - (ax[ddx0]/(ax[ddx0+1] - ax[ddx0]))*(t[ddx0+1] - t[ddx0])
            T = (t_2 - t_1)*2
            f.append(1/T)
            ddx0 = i

        
    return np.mean(f)

def diff_fase(ax, ay, t, f):

    ddx0 = -1
    dx = []
    dy = []
    #ax = ax - np.mean(ax)
    #ay = ay - np.mean(ay)

    for i in range(0, len(t) - 1):
        ddx = ax[i]*ax[i+1]
        ddy = ay[i]*ay[i+1]

        if ax[i] < 0 and ax[i+1] > 0:
            t_0 = t[i] - (ax[i]/(ax[i+1] - ax[i]))*(t[i+1] - t[i])
            dx.append(t_0)

        if ay[i] < 0 and ay[i+1] > 0:
            t_0 = t[i] - (ay[i]/(ay[i+1] - ay[i]))*(t[i+1] - t[i])
            dy.append(t_0)
        # if ddx < 0:
        #     t_0 = t[i] - (ax[i]/(ax[i+1] - ax[i]))*(t[i+1] - t[i])
        #     dx.append(t_0)
        #
        # if ddy < 0:
        #     t_0 = t[i] - (ay[i]/(ay[i+1] - ay[i]))*(t[i+1] - t[i])
        #     dy.append(t_0)

    delta = [] 
    T = 1.0 / f
    for i in range(0, min(len(dx), len(dy))):
        diff_bruta = dx[i] - dy[i]
        
        delta_t = ((diff_bruta + T/2) % T) - T/2
        
        delta.append(delta_t)

    return np.mean(delta)

def amplitude(ax, t):
    max_x = max(ax)

    ax_centered = ax - np.mean(ax)
    rms = np.sqrt(np.mean(ax_centered**2))

    amplitude_rms = rms * np.sqrt(2)
    
    amplitude = amplitude_rms + np.mean(ax)

    return amplitude

def desinclinar_sinal(ax, ay,az):
    G_x = np.mean(ax)
    G_y = np.mean(ay)
    G_z = np.mean(az)
    
    g_total = np.sqrt(G_x**2 + G_y**2 + G_z**2)
    
    sinal_x = np.sign(G_x) if G_x != 0 else 1
    sinal_y = np.sign(G_y) if G_y != 0 else 1
    sinal_z = np.sign(G_z) if G_z != 0 else 1

    theta = np.arcsin(np.abs(G_x) / g_total)
    phi = np.arctan2(np.abs(G_z), np.abs(G_y))
    
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    cos_p, sin_p = np.cos(phi), np.sin(phi)
    
    ax_corrigido = cos_t * ax - (sinal_x * sinal_z * sin_t) * az
    
    ay_corrigido = (sinal_x * sinal_z * sin_t * sin_p) * ax + (sinal_y * cos_p) * ay + (sinal_z * sin_p * cos_t) * az
    az_corrigido = (sinal_x * sin_t * cos_p) * ax - (sinal_z * sin_p) * ay + (cos_t * cos_p) * az
    
    return ax_corrigido, ay_corrigido, az_corrigido 


def coss(amplitude_sinal, sinal_original, t, f, diff_fase_referencia=0):
    T = 1.0 / f
    w = 2 * m.pi * f
    
    pontos_no_periodo = np.where(t <= t[0] + T)[0]
    if len(pontos_no_periodo) == 0:
        pontos_no_periodo = range(0, min(100, len(t)))
        
    idx_pico = pontos_no_periodo[np.argmax(sinal_original[pontos_no_periodo])]
    t_pico = t[idx_pico]
    
    if diff_fase_referencia == 0:
        fase_out = -w * t_pico
        
        fase_out = ((fase_out + m.pi) % (2 * m.pi)) - m.pi
    else:
        fase_base_x = -w * t_pico
        fase_out = fase_base_x + diff_fase_referencia
        fase_out = ((fase_out + m.pi) % (2 * m.pi)) - m.pi

    return amplitude_sinal, fase_out

def analisar_acelerometro(arquivo):
    data = np.loadtxt(arquivo, skiprows=1)
    
    t = data[:, 0]
    ax = data[:, 1]
    ay = data[:, 2]
    az = data[:, 3]

    #Tratamento do sinal 
    #(interpolacao cubica)
    #plot_compare2(ax,t,t)
    va.vel_atr(ax, ay, az, t)
    
    # va.vel_atr(ax, ay, az, t)
    #ax, ay, az = desinclinar_sinal(ax, ay, az)
    # g = m.sqrt(gx**2 + gy**2 + gz**2)
    # gx = np.mean(ax)
    # gy = np.mean(ay)
    # gz = np.mean(az)

    # ax = ax - gx
    # ay = ay - gy
    # az = az - gz

    #plot_compare2(ax,t,t)

    #A = amplitude(ax, t)
    #B = amplitude(ay, t)
    
    #R= np.arctan2(ay, ax)
    #plot_compare2(R,(t)*0,t)
    



    #diff_fase(ax, ay, t)
    # fx = freq(ax, t)
    # fy = freq(ax, t)
    # fase = diff_fase(ax, ay, t, fx)
    # print("Diferenca de fase", fase*fx*360)

    # print("A: ", A)
    # print("B: ", B)
    # angulo = m.atan2(A,B)*180/m.pi
    # angulo = angulo
    # print("Angulo força: ", angulo)
    # w = 2 * np.pi * fx
    # #
    # # angulo = m.degrees(m.atan2(A, B))
    # # fase = (fase_x - fase_y)*180/np.pi
    # #
    # print("============== VEL Prod =========================")
    # print("Vel Prod 1.0")
    # # shi = calculate_phase_shift(t, ax, ay)
    # # print("phase_shift: ", shi)
    # #
    # A, fase_x = coss(A, ax, t,fx, 0)
    # B, fase_y = coss(B, ay, t, fx, fase)
    # print(f"--- Funções do Acelerômetro (Frequência: {fx:.2f} Hz) ---")
    # print(f"w = {w:.4f} rad/s")
    # print(f"ax = {A:.4f} * cos({w:.4f}t + {fase_x:.4f})")
    # print(f"ay = {B:.4f} * cos({w:.4f}t + {fase_y:.4f})")
    # print(f"Diferença de fase: {fase:.2f}")

    # print("")
    # vp.vel_prod(A,B,fx,fase_x, fase_y)

    #plot_integral(A,B,fase_x, fase_y, f_maior)


if __name__ == "__main__":
    print("==================== Calha Boa 1=========================")
    analisar_acelerometro('./dados/b_1.txt')
    print("==================== Calha Boa 2=========================")
    analisar_acelerometro('./dados/b_2.txt')
    print("==================== Calha Boa 3=========================")
    analisar_acelerometro('./dados/b_3.txt')
    print("\n\n")


    print("==================== Calha Ruim 1=========================")
    analisar_acelerometro('./dados/r_1.txt')

    print("==================== Calha Ruim 2=========================")
    analisar_acelerometro('./dados/r_2.txt')

    print("==================== Calha Ruim 3=========================")
    analisar_acelerometro('./dados/r_3.txt')
