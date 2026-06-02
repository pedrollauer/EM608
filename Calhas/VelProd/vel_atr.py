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

def _input(texto:str=""):
    if _debug:
        r = input(texto)
        return r
    return ""

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

def forca_atrito_est(ax,mu, m_s, m_prod, N, dir_vel):
    """
    ESTE MÈTODO CALCULA A FORCA DE ATRITO E RETORNA UM VETOR
    O PRIMEIRO TERMO É 1 SE O ATRITO É ESTÁTICO E -1 SE O A-
    TRITO É DINÂMICO E ZERO SE O PRODUTO DECOLOU TOTALMENTE.
    O SEGUNDO TERMO CONTEM O VALOR DA FORÇA DE ATRITO COM O 
    SENTIDO.

    ax      - ACELERACAO EM X
    mu      - COEFICIENTE DE ATRITO ESTÁTICO
    m_s     - COEFICIENTE DE ATRITO DINÂMICO
    m_prod      - MASSA
    N       - FORÇA NORMAL
    dir_vel - DIREÇÃO DA VELOCIDADE

    """
    Fat_lim = N*mu
    Fat = m_prod*ax
    if N < 0:
        return 0,0

    if(dir_vel != 0 or abs(Fat) > Fat_lim ):
        return -1 ,-np.sign(dir_vel)*m_s*N
    else:
        return 1,Fat

    
    return Fat


def plot_compare(ax,ay,t,t1):

    fig, ax1 = plt.subplots()
    
    ax1.plot(t, ax, color='blue', linewidth=2, label='X')
    ax1.plot(t1, ay, color='orange', linewidth=2, label='Y')

    ax1.set_title(f'Exp vs Trat', fontsize=14)
    ax1.set_ylabel('Amplitude (Original)', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right')
    
    plt.xlim(5, 5.1)
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

def integral(y,t):
    integral = integrate.cumulative_simpson(y,x=t, initial=0)
    integral = integral - np.mean(integral)

    return integral

def vel_atr(ax, ay, az,t, ciclos=0):
    print(" === VEL ATR === ")

    # Configurações
    mu = 0.5 # C atrito estático
    mu_c = mu*0.2 # C atrito dinâmico
    m_prod = 0.001 # Massa

    ss = sinal_estatico([ax, ay, az])

    #Tratamento do sinal
    ax = ax - ss[0]
    ay = ay - ss[1]
    az = az - ss[2]
    
    splx = CubicSpline(t, ax)
    sply = CubicSpline(t, ay)
    splz = CubicSpline(t, az)

    # aax = ax.copy()
    # aay = ay.copy()
    # ttt = t.copy()

    t = np.linspace(0, t[len(t)-1], len(t)*10)
    

    ax = splx(t)
    ay = sply(t)
    az = splz(t)

    
    svx = splx.antiderivative() 
    svy = sply.antiderivative() 

    vx = svx(t)
    vy = svy(t)

    ssx = svx.antiderivative() 
    ssy = svy.antiderivative() 

    sx = ssx(t)
    sy = ssy(t)

    #vx = vx #- np.mean(vx)

    #vx = integral(ax,t)
    #plot_compare2(vx,ax*0,t)

    #plot_compare(ay,aay,t,ttt)

    mass_acc = modulo(ss) 
    g = -9.81
    a_rel_prod = []
    v_rel = [] # Velocidade relativa do produto
    v_prod = [] # Velocidade absoluta
    s_prod = 0
    P = m_prod*g
    N = []
    F_at = []
    Fat_est = []

    Fat_din = 0
    descolado = False
    
    d_vel_x = 0 # SENTIDO VEL X ZERO SE O PRODUTO ESTÁ PARADO, 1 SE POSITIVO, -1 SE NEGATIVO
    
    ### CINEMÁTICA ABSOLUTA DO PRODUTO
    v_a_x = 0 # VELOCIDADE ABSOLUTA DE X NO INSTANTE QUE O PRODUTO PULA
    v_a_y = 0 # VELOCIDADE ABSOLUTA DE Y NO INSTANTE QUE O PRODUTO PULA
    s_a_y = 0 # POSICAO ABSOLUTA DE Y

    S_delize = 0
    S_voo = 0

    # Ciclo de simulação
    for i in range (0, len(t)):

        ### DINÂMICA ### 
        N.append(-P + m_prod*ay[i])
        fat = forca_atrito_est(ax[i], mu,mu_c, m_prod, N[i], d_vel_x)
        Fat_est.append(fat[1]) # FAT 

        ### PRINTS ###

        _print(f"=== PASSO {i} ===")
        _print(f"t: {t[i]}")
        _print(f"AX: {ax[i]}")
        _print(f"AY: {ay[i]}")
        _print(f"VX: {vx[i]}")
        _print(f"N: {N[i]}")
        FATMAX = N[i]*mu

        _print(f"FATMAX: {FATMAX}")
        _print(f"FADERENCIA: {m_prod*ax[i]}")
        _print(f"SPROD: {s_prod}")

        _print(f"g :  {g} m/s2")
        _print(f"P : {P} kg")
        _print(f"N : {P} kg")

        ### PRINTS ###

        ### Cinemática ###

        # PRODUTO DESCOLOU
        if fat[0] == 0 and descolado == False:
            descolado = True

            if i-1 >=0:
                v_a_x = vx[i] + v_rel[i-1]

            else:
                v_a_x = vx[i]

            v_a_y = vy[i]
            s_a_y = sy[i]
            # s_a_x = sx[i]

            v_rel.append(v_a_x-vx[i])
            _print(f"SAY: {s_a_y}")
            _input()
            continue 
        
        if(descolado == True):
            s_a_y += v_a_y*(t[i] - t[i-1]) + g*((t[i]**2 - 2*t[i]*t[i-1] +t[i-1]**2))/2
            v_a_y = v_a_y +g*(t[i] - t[i-1])
            v_rel.append(v_a_x - vx[i])

            if sy[i] < s_a_y:
                #s_prod += v_a_x*(t[i] -t[i-1])
                s_prod += v_rel[i]*(t[i] -t[i-1]) # MOVIMENTO RETILÍNEO UNIFORME EM X
                S_voo += v_rel[i]*(t[i] -t[i-1]) 
                continue

            #CONDIÇÃO DE RETORNO            
            if(sy[i] >= s_a_y):
                descolado = False
                d_vel_x = np.sign(v_rel[-1])
                fat = forca_atrito_est(ax[i], mu,mu_c, m_prod, N[i], d_vel_x)
                Fat_est[i] = fat[1]
                continue
                # s_prod += s_a_x - sx[i] # DIFERENÇA ENTRE A POSICAO EM QUE O PRODUTO DEIXOU E ENCONTROU A CALHA

        # PRODUTO PARADO EM RELAÇÃO À CALHA
        if(d_vel_x == 0 and descolado == False):

            # VEMOS SE O ATRITO É DINÂMICO
            if(fat[0] == -1):
                _print(f"{i} Produto descolou.")
                d_vel_x = (-1)*(np.sign(ax[i]))

            v_rel.append(0)
            continue

        # PRODUTO MOVENDO-SE EM RELAÇÃO À CALHA
        elif(descolado == False and i > 0): 
            a_rel = ((fat[1]/m_prod)-ax[i])
            v_rel.append(v_rel[i-1] + (t[i] - t[i-1])*(a_rel))
            s_prod += v_rel[i]*(t[i] - t[i-1])
            S_delize += v_rel[i]*(t[i] - t[i-1])

            # Condicao de parada
            if (v_rel[i-1] * v_rel[i]) < 0:
                v_rel[i] = 0 # PRODUTO PAROU A VELOCIDADE CALCULADA INICIALMENTE ESTÁ ERRADA E VALE ZERO
                _print(f"Produto colou.")
                d_vel_x = 0
            else:
                d_vel_x = np.sign(v_rel[i])
        ### Cinemática ###

    ### RESULTADOS FINAIS ###
    VELATR = s_prod/t[len(t)-1]

    print(f"VELATR: {VELATR*60} m/min")
    print(f"DELS DESLIZE: {S_delize} m")
    print(f"DESL VOO: {S_voo} m")
