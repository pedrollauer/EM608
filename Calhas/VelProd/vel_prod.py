import math as m
import sympy as sp
import numpy as np
from scipy.optimize import fsolve

_debug = False


def find_tv(t, w, td, B, g,b):
    y0 = -B * np.cos(w * td+b)/(w**2)
    v0 = B* np.sin(w * td+b)/(w)

    y_massa = y0 + v0*(t-td) - 0.5 * g * ((t-td)**2)
    y_mola = -B * np.cos(w * (t)+b)
    return y_massa - y_mola


def tempo_voo(td, w, B,g,b):
    for i in range(1,1000):
        t0 = 0.00001*i + td
        tn = 0.00001*(i+1) + td
        Sv0 = find_tv(t0, w, td, B, g,b)
        St_n = find_tv(tn, w, td, B, g,b)
        
        if(Sv0*St_n<0):
            tv = (t0+tn)/2
            return tv

def vel_atr2(A, B, f, a, b):
    print("============== VEL ATR =========================")
    mu_s = 0.30
    mu_k = mu_s*(0.75)
    mu = 0.5
    g = 9.8
    omega = f*2*m.pi

    # Solução de A cos(wt + a) = m_s (B cos(wt +b) + g)
    Cx = A * np.cos(a) - mu_s * B * np.cos(b)
    Cy = A * np.sin(a) - mu_s * B * np.sin(b)
    R = np.sqrt(Cx**2 + Cy**2)
    psi = np.arctan2(Cy, Cx)

    argument = (mu_s * g) / R
    if np.abs(argument) > 1.0:
        print("Essa massa nunca deve deslizar")
        return None

    # Sabemos o tempo de inicio de deslizamento
    t_start = (np.arccos(argument) - psi) / omega
    if t_start < 0:
        t_start += (2 * np.pi) / omega

    print(f"Tempo de Deslizamento: {t_start*1000:.4f} ms")
    # Verificar a necessidade de subtrair esse sin(a)
    V_x0 = (A / omega) * np.sin(omega * t_start + a) - (A / omega) * np.sin(a)

    def relative_velocity_equation(t):
        # Absolute mass velocity under continuous sliding
        V_m = V_x0 - mu_k * g * (t - t_start) - (mu_k * B / omega) * (np.sin(omega * t + b) - np.sin(omega * t_start + b))
        # Absolute plane velocity
        V_p = (A / omega) * np.sin(omega * t + a) - (A / omega) * np.sin(a)
        
        return V_m - V_p  # Returns relative velocity (must equal 0)

    # 3. Solve numerically using t_start + a small delta as the initial guess
    initial_guess = t_start + 0.05
    t_end = fsolve(relative_velocity_equation, x0=initial_guess)[0]
    t_ciclo = 1/60
    print(f"Tempo de FIM: {t_end*1000:.4f} ms")
    print(f"Tempo de ciclo: {t_ciclo*1000:.4f} ms")
    
    dt = t_end - t_start
    linear_term = (V_x0 + (mu_k * B / omega) * np.sin(omega * t_start + b)) * dt
    parabolic_term = -0.5 * mu_k * g * (dt ** 2)
    
    harmonic_B = (mu_k * B / (omega ** 2)) * (np.cos(omega * t_end + b) - np.cos(omega * t_start + b))
    harmonic_A = -(A / (omega ** 2)) * (np.cos(omega * t_end + a) - np.cos(omega * t_start + a)) - ((A / omega) * np.sin(a) * dt)
    
    # Total relative displacement
    x_slip_relative = linear_term + parabolic_term + harmonic_B + harmonic_A
    x_plane_dt = -(A / (omega ** 2)) * (np.cos(omega * t_end + a) - np.cos(omega * t_start + a)) - ((A / omega) * np.sin(a) * dt)
    X_mass_absolute = x_slip_relative + x_plane_dt
    vel_relative_avg = x_slip_relative / dt
    vel_atr = X_mass_absolute / dt

    print(f"Vel prod: {vel_atr * 60:.2f} m/min")



def vel_atr(A,B,f,a,b):
    print("============== VEL ATR =========================")
    ms = 1
    mu = 0.5
    mu_s = mu
    g = 9.8

    A1 = mu*B/g    
    B1 = A/g
    w = f*2*m.pi

    t_desl = -1
    t_fim = -1
    t_ciclo = 1/f

    # Encontrar o t de inicio
    for i in range (1, 1000):
        ti = 0.0001*i
        ti_n = 0.0001*(i+1)

        ay = B*np.cos(w*ti + b)
        ax = A*np.cos(w*ti + a)

        ay_n = B*np.cos(w*(ti_n) + b)
        ax_n = A*np.cos(w*(ti_n) + a)

        N = (ay+g)
        N_n  = (ay_n+g)

        SLIP = ax - N*mu_s 
        SLIP_n = ax_n - N*mu_s

        if(SLIP*SLIP_n < 0):
            print("t_desl: ", (ti+ti_n)/2)
            t_desl = (ti+ti_n)/2
            break

    # Temos o t de inicio.
    V_x0 = (A / w) * np.sin(w*t_desl+ a)  - (A /w) * np.sin(a)

    for i in range (1, 1000):
        ti = 0.0001*i
        ti_n = 0.0001*(i+1)

        

    print(f"Vel Inicio: {V_x0*60 : 2f} m/min")
    print(f"Tempo de Deslizamento: {t_desl*1000:.4f} ms")
    print(f"Tempo de Deslizamento: {t_fim*1000:.4f} ms")
    print(f"Tempo de Ciclo : {t_ciclo*1000:.4f} ms")


def vel_prod(A,B,f, a, b):
#Aceleração absoluta m/s2
    g = 9.81

#Amplitude da Aceleração

    w = f*2*m.pi

    r = (g /B)
    if(abs(r) > 1):
        print("Aceleração y insuficiente.")
        vel_atr(A,B,f,a,b)
        return

    td = (1/w)*(m.acos(g/B) +b)
    if td < 0:
        print("td negativo")
        td += (2 * m.pi) / w

    vel_atr(A,B,f,a,b)
    v0 = B*m.sin(w*td + b)/w +  B*m.sin(b)/w 
    tv = tempo_voo(td, w, B, g, b) # Tempo de vôo por métodos numéricos;

    sx_tv = -A*m.cos(w*(tv+td)+a)/(w**2) + A*m.cos(a)/(w**2)
    sx_td = -A*m.cos(w*(td)+a)/(w**2) + A*m.cos(a)/(w**2)
    vox = A*m.sin(w*(td) + a)/w + A*m.sin(a)/w


    vel_deslocamento_calha = sx_tv - sx_td
    vel_curso_produto = vox
    vel = (sx_tv - sx_td)/(tv+td) + vox

    deslocamento_produto = vel_curso_produto*(tv-td) + sx_tv-sx_td


# 1. Definições Simbólicas para Propagação de Erro
    A_s, B_s, f_s, g_s, tv_s, td_s = sp.symbols('A B f g tv td')
    sA, sB, sf = sp.symbols('sigma_A sigma_B sigma_f')
    w_s = 2 * sp.pi * f_s

# Definição das funções baseadas em aceleração senoidal: a(t) = A*sin(wt)
# v(t) = -(A/w)cos(wt) | s(t) = -(A/w^2)sin(wt)
    vox_s = (A_s / w_s) * sp.sin(w_s * td_s)
    sx_td_s = -(A_s / (w_s**2)) * sp.cos(w_s * td_s)
    sx_tv_s = -(A_s / (w_s**2)) * sp.cos(w_s * (tv_s + td_s))

# Equação alvo: vel = (sx_tv - sx_td + vox*tv) / (tv + td)
    vel_expr = (sx_tv_s - sx_td_s + vox_s * tv_s) / (tv_s + td_s)

    val_g = g
    val_f = f
    val_w = 2 * np.pi * val_f

# Componentes (Ajustadas para 70° com a horizontal)
    val_A = A
    val_B = A

# 3. Cálculo Numérico Preciso de td e tv
# td: instante onde B*sin(w*td) = g
    val_td = td

    val_tv  = tv

# 4. Cálculo das Sensibilidades (Derivadas Parciais)
# Mapeamento de valores para substituição
    subs_map = {A_s: val_A, B_s: val_B, f_s: val_f, g_s: val_g, tv_s: val_tv, td_s: val_td}

# Coeficientes de sensibilidade
    dv_dA = float(sp.diff(vel_expr, A_s).subs(subs_map))
    dv_dB = float(sp.diff(vel_expr, B_s).subs(subs_map))
    dv_df = float(sp.diff(vel_expr, f_s).subs(subs_map))

# 5. Propagação da Incerteza (GUM)
# Defina aqui as incertezas dos seus instrumentos/sensores
    err_A = 0.06  # m/s²
    err_B = 0.06  # m/s²
    err_f = 0.05 # Hz

    sigma_vel = np.sqrt((dv_dA * err_A)**2 + (dv_dB * err_B)**2 + (dv_df * err_f)**2)
    val_vel = float(vel_expr.subs(subs_map))

    erro_rel = (sigma_vel/vel)*100


    if(_debug == False):
        print("=== Velocidade ===")
        print(f"Aceleração calha X: {A:.2f} ")
        print(f"Aceleração calha Y: {B:.2f}")
        print(f"w: {w:.2f}")
        print(f"Tempo de Desprendimento (td): {val_td*1000:.4f} ms")
        print(f"Tempo de Voo (tv):            {val_tv*1000:.4f} ms")
        print(f"Velocidade Média [m/s]: {vel:.4f}")
        print(f"Incerteza Total (sigma): ±{sigma_vel:.5f} m/s")
        print(f"Vel prod: {vel * 60:.2f} ± {sigma_vel*60:.5f} m/min")
        print(f"Vel curso: {vel_curso_produto * 60:.2f} ± {sigma_vel*60:.5f} m/min")
        print(f"Vel deslocamento calha: {vel_deslocamento_calha * 60:.2f} ± {sigma_vel*60:.5f} m/min")
        print(f"Deslocamento produto: {deslocamento_produto:.4f} ± {sigma_vel*60:.5f} m/min")
        print(f"Erro relativo: {erro_rel:.2f}%")
        print("=== Erros ===")

    if(_debug):
        for i in range(1,1000):
            t0 = 0.00001*i + td
            tn = 0.00001*(i+1) + td
            Sv0 = find_tv(t0, w, td, B, g)
            St_n = find_tv(tn, w, td, B, g)
            
            if(Sv0*St_n<0):
                tv = (t0+tn)/2
                print(f"tv={tv}")
