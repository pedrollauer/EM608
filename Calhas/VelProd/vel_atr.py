import numpy as np
import time
import math as m
from scipy.interpolate import CubicSpline
import math as m
import matplotlib.pyplot as plt
import scipy.integrate as integrate

_debug = False

def print_graph(pos_prod_x:float, pos_prod_y:float, pos_c_x:float, pos_c_y:float):
    """
            Plotar produto e calha
    """

    # tamanho da figura
    #print(1*'\n')

    # fatores de escala
    f_c_x = 1
    f_c_y = 1
    f_p_x = 1
    f_p_y = 1

    # configs da imagem
    pad_x = 100
    pad_y = 20

    # config corpos rigidos
    l_calha = 10
    produto = '*'
    calha = ''
    
    # transformacoes
    pxc = int(pos_c_x)
    pyc = int(pos_c_y)

    pad_x = abs(pad_x + pxc)*" "
    pad_y = abs(pad_y + pyc)

    calha = pad_x + l_calha*"="

    num_l = pad_y +1
    
    plot = f'\033[{num_l}A'
    plot += pad_y*"\033[K\n"
    plot += "\033[K" + calha + "\n"

    print(plot, end="", flush=True)
    time.sleep(0.1)

def _print(texto:str=""):
    if _debug:
        print(texto)

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
    s_prod = 0
    P = ms*g
    N = [10]
    F_at = []
    Fat_est = []

    Fat_din = 0
    deslocando = False

    # Ciclo de simulação
    v_rel.append(0)
    for i in range (0, 1000):
        _print(f"=== PASSO {i} ===")
        _print(f"AX: {ax[i]}")
        _print(f"AY: {ay[i]}")
        _print(f"VX: {vx[i]}")
        _print(f"N: {N[i]}")
        FATMAX = N[i]*mu_s
        _print(f"FATMAX: {FATMAX}")
        _print(f"MAX: {ms*ax[i]}")
        _print(f"VELREL: {v_rel[i]}")
        _print(f"SPROD: {s_prod}")
        ### Cinemática
        _print(f"g :  {g} m/s2")
        _print(f"P : {P} kg")
        _print(f"N : {P} kg")

        # Estática
        if(deslocando == False):
            
            N.append(P - ms*ay[i])
            Fat_est.append(forca_atrito_est(ax[i], mu,mu_s, ms, N[i], v_rel[i]))

            if(Fat_est[i] == 0):
                _print(f"{i} Produto descolou.")
                deslocando = True
                Fat_est.append(forca_atrito_est(ax[i], mu,mu_s, ms, N[i], ax[i]))
                v_rel.append(0) ### O produto começa a deslocar com velocidade zero
                continue
            v_rel.append(0)
            continue

        # print("LENFAT: ", len(Fat_est))
        # print("LENVEL: ", len(v_rel))

        ### Dinâmica
        N.append(P - ms*ay[i])
        #v_rel = v_rel[i-1] - (Fat_est/ms)*t[i]
        v_rel.append(v_rel[i-1]+ (t[i] - t[i-1])*((Fat_est[i]/ms)-ax[i]))
        #Fat_est.append(forca_atrito_est(ax[i], mu,mu_s, ms, N[i], v_rel[i]))
        #Fat_est.append(mu_s*N[i]) 
        s_prod += v_rel[i]*(t[i]) - v_rel[i]*(t[i-1])
        # Condicao de parada
        if (v_rel[i-1] * v_rel[i]) <= 0:
            deslocando = False
            v_rel.append(0)
            _print(f"Produto colou")
        else:
            v_rel.append(v_rel[i])

    VELATR = s_prod/t[len(t)-1]
    print(f"VELATR: {VELATR*60} m/min")
