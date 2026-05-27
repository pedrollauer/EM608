import numpy as np
import math as m
from scipy.interpolate import CubicSpline
import math as m
import matplotlib.pyplot as plt
import scipy.integrate as integrate

_debug = True
def sinal_estatico(sinais):
    ss = []
    for i in range(0, len(sinais)):
        ss.append(np.mean(sinais[i]))
    return ss 

def modulo(vetor):
    g = 0
    for sinal in vetor:
        g = g + sinal**2

    if(g>0):
        return m.sqrt(g)
    else:
        return -1

def forca_atrito_est(ax,mu, m_s, ms, N, v_rel):
    if(v_rel != 0):
        return -np.sign(v_rel)*m_s*N
    Fat_lim = N*mu

    Fat = ms*ax

    if(abs(Fat) > Fat_lim):
        Fat = N*m_s
        return 0
    else:
        return Fat

    
    return Fat

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

def integral(y,t):
    integral = integrate.cumulative_simpson(y,x=t, initial=0)
    integral = integral - np.mean(integral)

    return integral

def vel_atr(ax, ay, az,t, ciclos=0):
    print(" === VEL ATR === ")

    # Configurações
    mu = 0.5 # C atrito estático
    mu_s = mu*0.2 # C atrito dinâmico
    ms = 0.001 # Massa

    ss = sinal_estatico([ax, ay, az])

    #Tratamento do sinal
    ax = ax - ss[0]
    ay = ay - ss[1]
    az = az - ss[2]
    
    splx = CubicSpline(t, ax)
    sply = CubicSpline(t, ay)
    splz = CubicSpline(t, az)

    t = np.linspace(0, t[len(t)-1], len(t)*10)

    ax = splx(t)
    ay = sply(t)
    az = splz(t)

    
    svx = splx.antiderivative() 
    vx = svx(t)
    vx = vx #- np.mean(vx)
    #vx = integral(ax,t)

    #plot_compare2(vx,ax*0,t)

    g = modulo(ss) 
    a_rel_prod = []
    v_rel = [] # Velocidade relativa do produto
    v_prod = [] # Velocidade absoluta
    P = ms*g
    N = []
    F_at = []
    Fat_est = []

    Fat_din = 0
    deslocando = False

    # Ciclo de simulação
    v_rel.append(0)
    for i in range (0, 1000):

        # Estática
        if(deslocando == False):
            
            N.append(P - ms*ay[i])
            Fat_est.append(forca_atrito_est(ax[i], mu,mu_s, ms, N[i], v_rel[i]))

            if(Fat_est[i] == 0):
                print(f"{i} Produto descolou.")
                deslocando = True
                Fat_est.append(forca_atrito_est(ax[i], mu,mu_s, ms, N[i], ax[i]))
                continue
            v_rel.append(0)
            continue

        ### Dinâmica
        N.append(P - ms*ay[i])
        #v_rel = v_rel[i-1] - (Fat_est/ms)*t[i]
        v_rel.append(v_rel[i-1]+ (t[i] - t[i-1])*((Fat_est[i]/ms)-ax[i]))
        Fat_est.append(forca_atrito_est(ax[i], mu,mu_s, ms, N[i], v_rel[i]))

        # Condicao de parada
        if (v_rel[i-1] * v_rel[i]) <= 0:
            deslocando = False
            v_rel.append(0)
        else:
            v_rel.append(v_rel[i])
        
        ### Cinemática
        if(_debug):
            print(f"===== PASSO {i} ======")
            print(f"g :  {g} m/s2")
            print(f"P : {P} kg")
            print(f"N : {P} kg")

