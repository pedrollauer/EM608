import math as m
import sympy as sp
import numpy as np
from scipy.optimize import fsolve

_debug = False

def erro(tv):
    # 1. Definições Simbólicas para Propagação de Erro
    A_s, B_s, f_s, g_s, tv_s, td_s = sp.symbols('A B f g tv td')
    sA, sB, sf = sp.symbols('sigma_A sigma_B sigma_f')
    w_s = 2 * sp.pi * f_s

    # Definição das funções baseadas em aceleração senoidal: a(t) = A*sin(wt)
    # v(t) = -(A/w)cos(wt) | s(t) = -(A/w^2)sin(wt)
    vox_s = -(A_s / w_s) * sp.cos(w_s * td_s)
    sx_td_s = -(A_s / (w_s**2)) * sp.sin(w_s * td_s)
    sx_tv_s = -(A_s / (w_s**2)) * sp.sin(w_s * (tv_s + td_s))

    # Equação alvo: vel = (sx_tv - sx_td + vox*tv) / (tv + td)
    vel_expr = (sx_tv_s - sx_td_s + vox_s * tv_s) / (tv_s + td_s)

    C = 50.0  # Aceleração absoluta
    val_g = 9.81
    val_f = 60.0
    val_w = 2 * np.pi * val_f
    
    # Componentes (Ajustadas para 70° com a horizontal)
    val_A = C * np.cos(np.radians(70))
    val_B = C * np.sin(np.radians(70))

    # 3. Cálculo Numérico Preciso de td e tv
    # td: instante onde B*sin(w*td) = g
    val_td = (1/val_w) * np.arcsin(val_g / (val_B * val_w**2))

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
    err_A = 0.1  # m/s²
    err_B = 0.1  # m/s²
    err_f = 0.05 # Hz

    sigma_vel = np.sqrt((dv_dA * err_A)**2 + (dv_dB * err_B)**2 + (dv_df * err_f)**2)
    val_vel = float(vel_expr.subs(subs_map))

    # 6. Output Formatado
    print(f"--- Relatório de Engenharia (Frequência: {val_f} Hz) ---")
    print(f"Tempo de Desprendimento (td): {val_td*1000:.4f} ms")
    print(f"Tempo de Voo (tv):            {val_tv*1000:.4f} ms")
    print(f"Velocidade Média (vel):       {val_vel:.5f} m/s")
    print(f"Incerteza Total (sigma):     ±{sigma_vel:.5f} m/s")
    print(f"Produção Estimada:            {val_vel * 60:.2f} m/min")
    print("-" * 45)


def find_tv(t, w, td, B, g):
    y0 = B * np.cos(w * td)/(w**2)
    v0 = -B* np.sin(w * td)/(w)

    y_massa = y0 + v0*(t-td) - 0.5 * g * ((t-td)**2)
    y_mola = B * np.cos(w * (t))
    return y_massa - y_mola


def tempo_voo(td, w, B,g):
    for i in range(1,1000):
        t0 = 0.00001*i + td
        tn = 0.00001*(i+1) + td
        Sv0 = find_tv(t0, w, td, B, g)
        St_n = find_tv(tn, w, td, B, g)
        
        if(Sv0*St_n<0):
            tv = (t0+tn)/2
            return tv

def vel_prod():
#Aceleração absoluta m/s2
    C = 50
    g = 9.81

#Amplitude da Aceleração
    A = C * m.sin(m.radians(70)) 
    B = C * m.cos(m.radians(70))

#Ax = A*m.cos(w*t)
#Ay = B*m.cos(w*t)

    f = 60
    w = f*2*m.pi

    r = g / (B * (w**2))
    if(abs(r) > 1):
        print("Aceleração y insuficiente.")

    td = (1/w)*m.acos(g/(B*(w**2)))
    v0 = B*m.sin(w*td)/w
    tv = 4*abs(v0)/g # Tempo de vôo por Taylor 4º grau. Erro alto, evitar.
    tv = tempo_voo(td, w, B, g) # Tempo de vôo por métodos numéricos;

    sx_tv = -A*m.cos(w*(tv+td))/(w**2)
    sx_td = -A*m.cos(w*(td))/(w**2)
    vox = A*m.sin(w*(td))/w

    vel = (sx_tv - sx_td + vox*tv)/(tv+td)


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
    err_A = 0.1  # m/s²
    err_B = 0.1  # m/s²
    err_f = 0.05 # Hz

    sigma_vel = np.sqrt((dv_dA * err_A)**2 + (dv_dB * err_B)**2 + (dv_df * err_f)**2)
    val_vel = float(vel_expr.subs(subs_map))

    erro_rel = (sigma_vel/vel)*100


    if(_debug == False):
        print("============== VEL Prod =========================")
        print("Vel Prod 1.0")
        print("=== Velocidade ===")
        print(f"Aceleração calha X: {A:.2f} ")
        print(f"Aceleração calha Y: {B:.2f}")
        print(f"w: {w:.2f}")
        print(f"Tempo de Desprendimento (td): {val_td*1000:.4f} ms")
        print(f"Tempo de Voo (tv):            {val_tv*1000:.4f} ms")
        print(f"Velocidade Média [m/s]: {vel:.4f}")
        print(f"Incerteza Total (sigma): ±{sigma_vel:.5f} m/s")
        print(f"Vel prod: {vel * 60:.2f} ± {sigma_vel*60:.5f} m/min")
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


