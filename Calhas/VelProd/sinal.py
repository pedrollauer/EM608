import numpy as np
from scipy.fft import fft, fftfreq
import vel_prod as vp
import math as m

def analisar_acelerometro(arquivo):
    data = np.loadtxt(arquivo, skiprows=1)
    
    t = data[:, 0]
    ax = data[:, 1]
    ay = data[:, 2]
    az = data[:, 3]
    
    tratado = "Sinal tratado."
    #O sinal está tratado?
    # media = np.mean(ay)
    # if(media > 1):
    #     tratado = "Sinal não tratado."
    #     ax = ax - np.mean(ax)
    #     ay = ay - np.mean(ay)
    #     az = az - np.mean(ay)

    # print(f"Dado tratado: {media}")
    # n = len(t)
    # dt = t[1] - t[0]  
    #FIM TRATAMENTO
    

    def obter_dominante_2(time_array, acceleration_array, target_frequency_hz=60):
        omega = 2 * np.pi * target_frequency_hz
        N = len(time_array)
        
        # 1. Eliminate the DC offset (Zero-center the data)
        A_offset = np.mean(acceleration_array)
        ay_centered = acceleration_array - A_offset
        
        # 2. Project the ZERO-CENTERED data onto orthogonal components
        Cx = (2.0 / N) * np.sum(ay_centered * np.cos(omega * time_array))
        Cy = -(2.0 / N) * np.sum(ay_centered * np.sin(omega * time_array))
        
        # 3. Convert back to polar Amplitude and Phase
        A = np.sqrt(Cx**2 + Cy**2)
        alpha = np.arctan2(-Cy, Cx)
        A = A + A_offset
        
        return 60,A, alpha,



    def obter_dominante(sinal):
        yf = fft(sinal)
        xf = fftfreq(n, dt)
        
        pos_mask = xf > 0
        xf_pos = xf[pos_mask]
        yf_pos = np.abs(yf[pos_mask])
        
        idx_max = np.argmax(yf_pos)
        f_Hz = xf_pos[idx_max]
        
        amplitude = 2.0 * np.abs(yf[pos_mask][idx_max]) / n
        fase = np.angle(yf[pos_mask][idx_max])
        
        return f_Hz, amplitude, fase

    f_maior, A, fase_x = obter_dominante_2(t,ax)
    _, B, fase_y = obter_dominante_2(t,ay)
    _, C, fase_z = obter_dominante_2(t,az)
    
    # f_maior, A, fase_x = obter_dominante(ax)
    # _, B, fase_y = obter_dominante(ay)
    # _, C, fase_z = obter_dominante(az)

    w = 2 * np.pi * f_maior
    
    angulo = m.degrees(m.atan2(A, B))
    fase = (fase_x - fase_y)*180/np.pi
    
    print("============== VEL Prod =========================")
    print("Vel Prod 1.0")

    print(f"--- Funções do Acelerômetro (Frequência: {f_maior:.2f} Hz) ---")
    print(f"w = {w:.4f} rad/s")
    print(f"ax = {A:.4f} * cos({w:.4f}t + {fase_x:.4f})")
    print(f"ay = {B:.4f} * cos({w:.4f}t + {fase_y:.4f})")
    print(f"az = {C:.4f} * cos({w:.4f}t + {fase_z:.4f})")
    print(f"Ângulo de aplicação de força: {angulo: 2f}")

    print(f"Diferença de fase: {fase:.2f}")
    print(f"Condicionamento do sinal: {tratado}")

    print("")
    vp.vel_prod(A,B,f_maior,fase_x, fase_y)

if __name__ == "__main__":
    print("==================== Calha Boa 1=========================")
    analisar_acelerometro('./dados/b_1.txt')
    print("\n\n")
    print("==================== Calha Boa 2=========================")
    analisar_acelerometro('./dados/b_2.txt')
    print("\n\n")
    print("==================== Calha Boa 3=========================")
    analisar_acelerometro('./dados/b_3.txt')
    print("\n\n")

    print("==================== Calha Ruim 1=========================")
    analisar_acelerometro('./dados/r_1.txt')

    print("==================== Calha Ruim 2=========================")
    analisar_acelerometro('./dados/r_2.txt')

    print("==================== Calha Ruim 3=========================")
    analisar_acelerometro('./dados/r_3.txt')
