# coding=utf-8
import math
import matplotlib.pyplot as plt
import numpy as np

def calcular_largura_chaveta(d):
    if 0.312 < d <= 0.437:
        return 0.093 
    if 0.437 < d <= 0.562:
        return 0.125 
    if 0.562 < d <= 0.875:
        return 0.187 
    if 0.875 < d <= 1.250: 
        return 0.250 
    if 1.250 < d <= 1.375: 
        return 0.312 
    if 1.375 < d <= 1.750: 
        return 0.375 
    if 1.750 < d <= 2.250: 
        return 0.500 
    if 2.250 < d <= 2.750: 
        return 0.625 
    if 2.750 < d <= 3.250: 
        return 0.750 
    if 3.250 < d <= 3.750: 
        return 0.875 
    if 3.750 < d <= 4.500: 
        return 1.000 
    if 4.500 < d <= 5.500: 
        return 1.250 
    if 5.500 < d <= 6.500: 
        return 1.500 

def in_para_mm(comprimento_in):
    # 1 in é igual a 25.4 mm
    return comprimento_in * 25.4

def lb_para_N(forca_lb):
      return forca_lb * 4.44822

def c_carga():
    return 1

# TODO: Colocar a fórmula para a chaveta
def Kts(D,d,r):
    Dd = np.array([2.0, 1.33, 1.20, 1.09])
    A = np.array([0.86331, 0.84897, 0.83425, 0.90337])
    b = np.array([-0.23865, -0.23161, -0.21649, -0.12692])


    razao_d = float(D)/float(d)
    for i in range(0, Dd.size):
       if razao_d == Dd[i]:
           return A[i]*(r/d)**b[i]
       elif Dd[i] < razao_d:
           A_r = (A[i-1]-A[i])/(Dd[i-1] - Dd[i])*(razao_d-Dd[i]) + A[i]
           b_r = (b[i-1]-b[i])/(Dd[i-1] - Dd[i])*(razao_d-Dd[i]) + b[i]
           return A_r*(r/d)**b_r

# TODO: Colocar a fórmula para a chaveta
def Kts_chaveta(D,d,r):
    x = r/d
    y = 5*(10**8)*x**6 - (10**8)*x**5 + 9*(10**6)*x**4 - 463265*x**3 + 14630*x**2 - 285.03*x + 5.4414
    return y
def Kt_chaveta(D,d,r):
    x=r/d
    y = 5.611376 - 391.6429*x + 14691.66*(x**2) - 152944.8*(x**3) - 2992495*(x**4) + 54559890*(x**5)
    return y

def Kt(D,d,r):
    Dd = np.array([6.0, 3.0,2.0,1.5,1.2,1.1,1.07, 1.05, 1.02, 1.01])
    A = np.array([0.87868, 0.89334, 0.90879, 0.93836, 0.97098, 0.95120, 0.97527, 0.98137, 0.98061,0.96048, 0.91938])
    b = np.array([-0.33243, -0.30860, -0.28598, -0.25759, -0.21796, -0.23757,-0.20958, -0.19653, -0.18381, -0.17711, -0.17032])
    razao_d = float(D)/float(d)
    for i in range(0, Dd.size):
       if razao_d == Dd[i]:
           return A[i]*(r/d)**b[i]
       elif Dd[i] < razao_d:
           A_r = (A[i-1]-A[i])/(Dd[i-1] - Dd[i])*(razao_d-Dd[i]) + A[i]
           b_r = (b[i-1]-b[i])/(Dd[i-1] - Dd[i])*(razao_d-Dd[i]) + b[i]
           return A_r*(r/d)**b_r


def c_confiabilidade(confiabilidade):
    Conf = np.array([50, 90, 99, 99.9, 99.99, 99.999])
    C_conf = np.array([1, 0.897, 0.814, 0.753, 0.702, 0.659])

    for i in range(0,Conf.size):
        if confiabilidade == Conf[i]:
            return C_conf[i]
    
def c_temperatura():
    return 1

def nm_para_lb_in(momento_nm):
    # 1 N·m é igual a aproximadamente 8.85074 lb·in
    return momento_nm * 8.85074
#O segundo argumento é:
# 0 - Ground
# 1 - Usinado
# 2 - Laminado
# 3 - Forjado

def c_superficie(Sut, metodo):
    A = np.array([1.34, 2.7, 14.4, 39.9])
    b = np.array([-0.085, -0.265, -0.718, -0.995])
    c_surf = A[metodo]*(Sut)**b[metodo] 
    if c_surf > 1:
        return 1
    else:
        return c_surf

def c_tamanho(diametro):
    if diametro <= 0.3:
        return 1
    elif diametro> 0.3 and diametro < 10:
        return 0.869*diametro**(-0.097)
    else:
        return 0.6

def neuber(Sut):
   
   S = np.array([50, 55, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 180, 200, 220, 240])
   sqrt_a = np.array([0.130, 0.118, 0.108, 0.093, 0.080, 0.070, 0.062, 0.055, 0.049,0.044, 0.039, 0.031, 0.024, 0.018, 0.013, 0.009])

   if Sut < 50:
       return 0
   for i in range(0, S.size):
       if Sut == S[i]:
           return sqrt_a[i]
       elif S[i] > Sut:
           return (sqrt_a[i-1]-sqrt_a[i])/(S[i-1] - S[i])*(Sut-S[i]) + sqrt_a[i]

    ##const_neuber = 6.89476*

def Se_corrigir(Sut, diametro):
    Se_linha = 0.5*Sut
    return c_carga()*c_tamanho(diametro)*c_superficie(Sut,1)*c_temperatura()*c_confiabilidade(50)*Se_linha

def diametro_torsao_variavel(Mm, Ma, Ta, Tm, Sut,N,raio_escalonamento, d_chute, D_chute, chaveta):
    q = 1/(1+(neuber(Sut)/math.sqrt(raio_escalonamento)))
    qs = 1/(1+(neuber(Sut+20)/math.sqrt(raio_escalonamento)))

    Se_linha = 0.5*Sut
    Se = c_carga()*c_tamanho(d_chute)*c_superficie(Sut,1)*c_temperatura()*c_confiabilidade(50)*Se_linha

    D_chute = d_chute + 10*d_chute/100


    kf = 1 + q*(Kt(D_chute, d_chute,raio_escalonamento)-1)
    kfs  = 1 + qs*(Kts(D_chute, d_chute,raio_escalonamento)-1)

    if(chaveta == 1):
        kf_c = 1 + q*(Kt_chaveta(D_chute, d_chute,raio_escalonamento)-1)
        kfs_c = 1 + qs*(Kts_chaveta(D_chute, d_chute,raio_escalonamento)-1)

        if kf_c > kf:
            kf = kf_c
        elif kfs_c > kfs:
            kfs = kfs_c
    A = ((math.sqrt((kf*Ma)**2 +(3/4)*(kfs*Ta)**2))/(1000*Se) + (math.sqrt((kf*Mm)**2 + (3/4)*(kfs*Tm)**2))/(1000*Sut))
    return  math.pow((32*N/math.pi)*A,1.0/3.0)

def diametro_torsao_constante(M, Sut, T, Sy,N, d_chute, D_chute, chaveta):
    q = 1/(1+(neuber(Sut)/math.sqrt(raio_escalonamento)))
    qs = 1/(1+(neuber(Sut+20)/math.sqrt(raio_escalonamento)))

    Se_linha = 0.5*Sut
    Se = c_carga()*c_tamanho(d_chute)*c_superficie(Sut,1)*c_temperatura()*c_confiabilidade(50)*Se_linha

    D_chute = d_chute + 20*d_chute/100
    kf = 1 + q*(Kt(D_chute, d_chute,raio_escalonamento)-1)
    kfs  = 1 + qs*(Kts(D_chute, d_chute,raio_escalonamento)-1)

    if(chaveta == 1):
        kf_c = 1 + q*(Kt_chaveta(D_chute, d_chute,raio_escalonamento)-1)
        kfs_c = 1 + qs*(Kts_chaveta(D_chute, d_chute,raio_escalonamento)-1)

        if kf_c > kf:
            kf = kf_c
        elif kfs_c > kfs:
            kfs = kfs_c
    return  ((32*N/math.pi)*((kf*M/(Se*1000))**(2.0)+0.75*(kfs*T/(Sy*1000))**(2.0))**(0.5))**(1.0/3.0) 

def f_s(x, L, n):
    if n>=1:
        if x > L:
            return (x-L)**n
        else :
            return 0

print("Eixo")
# Nesse programa o eixo transmite uma potência P.
# Conhecemos a velocidade angular do eixo.
# Conhecemos o coeficiênte de segurança.

#Dados iniciais
L1 = 60/1000
L2 = 80/1000
L3 = 150/1000
L4 = 80/1000
L5 = 60/1000
L6 = 40/1000
Ld2 = 8/1000
Ld3 = 26/1000
Ld5 = 20/1000

P = 10*550*12 # in in-lb/s

v_min = 0.95 #m/s
v_max = 2 #m/s
v_g2 = 1.73 #m/s

diametro_primitivo_g1 = 150.0
diametro_primitivo_g2 = 200
diametro_polia = 100

w_min = v_min/(diametro_polia/2000) #rad/s
w_max = v_max/(diametro_polia/2000) #rad/s

w_g2 = v_g2/(diametro_polia/2000) #rad/s

N = 4
r_polia = diametro_polia/2/25.4 #in
angulo_pressao_engrenagem = 20*(math.pi/180) # rads
r_engrenagem = (diametro_primitivo_g1/2)/25.4 #in
r_engrenagem_g2 = (diametro_primitivo_g2/2)/25.4 #in


tamanho_viga = L1+L2+L3+L4+L5+L6

print("Tamanho_viga: %s",tamanho_viga)
### Tensão de Ruptura
Sut = 90.94#kpsi
Sy = 77.01#kpsi

#Calculo do torque.
T_min = P/w_max #lb in
T_max = P/w_min #lb in

T_g2 = P/w_g2
#### Polia ####

#Calculo da resultante na polia:
Fn_min = T_min/r_polia #lb
Fn_max = T_max/r_polia #lb
Fn_g2 = T_g2/r_polia

# Força do lado solto
# F2_min = T_min/(4*r_polia)
# F2_max = T_max/(4*r_polia)
# F2_g2 = T_g2/(4*r_polia)

# Força do lado apertado
# Assumindo uma correia tipo V
# F1_min = 1.5*F2_min
# F1_max  = 1.5*F2_max
# F1_g2  = 1.5*F2_g2

#Força de apoio na polia
# Fs_min = F1_min + F2_min
# Fs_max = F1_max + F2_max
# Fs_g2 = F1_g2 + F2_g2

Fs_min = 1.5*Fn_min
Fs_max = 1.5*Fn_max
Fs_g2 = 1.5*Fn_g2

#### Engrenagem ####

F_tan_min = T_min/r_engrenagem
F_tan_max = T_max/r_engrenagem
F_tan_g2 = T_g2/r_engrenagem_g2

F_rad_min = F_tan_min*math.tan(angulo_pressao_engrenagem)
F_rad_max = F_tan_max*math.tan(angulo_pressao_engrenagem)
F_rad_g2 = F_tan_g2*math.tan(angulo_pressao_engrenagem)

#### Obtenção dos diagramas ####

F_engrenagem_min= np.array([0,F_rad_min, (-1)*F_tan_min])
F_engrenagem_max = np.array([0,F_rad_max, (-1)*F_tan_max])
F_engrenagem_g2 = np.array([0,F_rad_g2, (-1)*F_tan_g2])

F_polia_min = np.array([0,0,(-1)*Fs_min])
F_polia_max = np.array([0, 0,(-1)*Fs_max])
F_polia_g2 = np.array([0, 0,(-1)*Fs_g2])

tamanho_x = 1000
passo = tamanho_viga/tamanho_x

x = np.zeros(tamanho_x)

acumulador = 0
### Pontos para o eixo
for i in range(0, tamanho_x):
               acumulador = acumulador + passo
               x[i] = acumulador

Mx_med = np.zeros(tamanho_x)
My_med = np.zeros(tamanho_x)
Mz_med = np.zeros(tamanho_x)
MM_med = np.zeros(tamanho_x)

Mx_alt = np.zeros(tamanho_x)
My_alt = np.zeros(tamanho_x)
Mz_alt = np.zeros(tamanho_x)
MM_alt = np.zeros(tamanho_x)


Mx_g2 = np.zeros(tamanho_x)
My_g2 = np.zeros(tamanho_x)
Mz_g2 = np.zeros(tamanho_x)
MM_g2 = np.zeros(tamanho_x)

MM_medio = np.zeros(tamanho_x)
MM_alternado = np.zeros(tamanho_x)


b = (L2+L3+L4)/25.4#in
p = (L2 - Ld2)/25.4#in
p_g2 = (L2 + L3 - Ld3)/25.4
q = (L2+L3+L4+L5+Ld5)/25.4#in

b_mm = L2 + L3 + L4
p_mm = L2 - Ld2
p_g2mm = (L2 + L3 - Ld3)
q_mm = L2 + L3 + L4 + L5 + Ld5
print("b",b)
print("p",p)
print("q",q)

R2_min = -(1/b)*(F_engrenagem_min*p + F_polia_min*q)
R2_max = -(1/b)*(F_engrenagem_max*p + F_polia_max*q)
R2_g2 = -(1/b)*(F_engrenagem_g2*p_g2 + F_polia_g2*q)

R1_min = -(R2_min + F_engrenagem_min + F_polia_min)
R1_max = -(R2_max + F_engrenagem_max + F_polia_max)
R1_g2 = -(R2_g2 + F_engrenagem_g2 + F_polia_g2)

#Mudança de unidade para facilicar a visualização gráfica
R1_min_N = lb_para_N(R1_min)
R2_min_N = lb_para_N(R2_min)
F_engrenagem_min_N = lb_para_N(F_engrenagem_min)
F_polia_min_N = lb_para_N(F_polia_min)

R1_max_N = lb_para_N(R1_max)
R2_max_N = lb_para_N(R2_max)
F_engrenagem_max_N = lb_para_N(F_engrenagem_max)
F_polia_max_N = lb_para_N(F_polia_max)


R1_g2_N = lb_para_N(R1_g2)
R2_g2_N = lb_para_N(R2_g2)
F_engrenagem_g2_N = lb_para_N(F_engrenagem_g2)
F_polia_g2_N = lb_para_N(F_polia_g2)

R1_med = (R1_max + R1_min)/2
R1_alt = (R1_max - R1_min)/2

R2_med = (R2_max + R2_min)/2
R2_alt = (R2_max - R2_min)/2

R2_med_N = lb_para_N(R2_med)
R2_alt_N = lb_para_N(R2_alt)
R1_med_N = lb_para_N(R1_med)
R1_alt_N = lb_para_N(R1_alt)

F_engrenagem_med_N = (F_engrenagem_max_N + F_engrenagem_min_N)/2
F_engrenagem_alt_N = (F_engrenagem_max_N - F_engrenagem_min_N)/2

F_polia_med_N = (F_polia_max_N + F_polia_min_N)/2
F_polia_alt_N = (F_polia_max_N - F_engrenagem_min_N)/2

for i in range(0,tamanho_x):
    Mx_med[i] = R1_med_N[0]*f_s(x[i], L1,1) + F_engrenagem_med_N[0]*f_s(x[i], p_mm+L1, 1) + R2_med_N[0]*f_s(x[i], b_mm+L1,1) + F_polia_med_N[0]*f_s(x[i], q_mm+L1, 1)
    My_med[i] = R1_med_N[1]*f_s(x[i], L1,1) + F_engrenagem_med_N[1]*f_s(x[i], p_mm+L1, 1) + R2_med_N[1]*f_s(x[i], b_mm+L1,1) + F_polia_med_N[1]*f_s(x[i], q_mm+L1, 1)
    Mz_med[i] = R1_med_N[2]*f_s(x[i], L1,1) + F_engrenagem_med_N[2]*f_s(x[i], p_mm+L1, 1) + R2_med_N[2]*f_s(x[i], b_mm+L1,1) + F_polia_med_N[2]*f_s(x[i], q_mm+L1, 1)
    MM_med[i] = math.sqrt(Mx_med[i]*Mx_med[i] + My_med[i]*My_med[i] + Mz_med[i]*Mz_med[i])

    Mx_alt[i] = R1_alt_N[0]*f_s(x[i], L1,1) + F_engrenagem_alt_N[0]*f_s(x[i], p_mm+L1, 1) + R2_alt_N[0]*f_s(x[i], b_mm+L1,1) + F_polia_alt_N[0]*f_s(x[i], q_mm+L1, 1)
    My_alt[i] = R1_alt_N[1]*f_s(x[i], L1,1) + F_engrenagem_alt_N[1]*f_s(x[i], p_mm+L1, 1) + R2_alt_N[1]*f_s(x[i], b_mm+L1,1) + F_polia_alt_N[1]*f_s(x[i], q_mm+L1, 1)
    Mz_alt[i] = R1_alt_N[2]*f_s(x[i], L1,1) + F_engrenagem_alt_N[2]*f_s(x[i], p_mm+L1, 1) + R2_alt_N[2]*f_s(x[i], b_mm+L1,1) + F_polia_alt_N[2]*f_s(x[i], q_mm+L1, 1)
    MM_alt[i] = math.sqrt(Mx_alt[i]*Mx_alt[i] + My_alt[i]*My_alt[i] + Mz_alt[i]*Mz_alt[i])

    Mx_g2[i] = R1_g2_N[0]*f_s(x[i], L1,1) + F_engrenagem_g2_N[0]*f_s(x[i], p_g2mm+L1, 1) + R2_g2_N[0]*f_s(x[i], b_mm+L1,1) + F_polia_g2_N[0]*f_s(x[i], q_mm+L1, 1)
    My_g2[i] = R1_g2_N[1]*f_s(x[i], L1,1) + F_engrenagem_g2_N[1]*f_s(x[i], p_g2mm+L1, 1) + R2_g2_N[1]*f_s(x[i], b_mm+L1,1) + F_polia_g2_N[1]*f_s(x[i], q_mm+L1, 1)
    Mz_g2[i] = R1_g2_N[2]*f_s(x[i], L1,1) + F_engrenagem_g2_N[2]*f_s(x[i], p_g2mm+L1, 1) + R2_g2_N[2]*f_s(x[i], b_mm+L1,1) + F_polia_g2_N[2]*f_s(x[i], q_mm+L1, 1)
    MM_g2[i] = math.sqrt(Mx_g2[i]*Mx_g2[i] + My_g2[i]*My_g2[i] + Mz_g2[i]*Mz_g2[i])

    # MM_alternado[i] = (MM_max[i] - MM_min[i])/2
    # MM_medio[i] = (MM_max[i] + MM_min[i])/2
MM_alternado = MM_alt
MM_medio = MM_med

plt.plot(x,MM_med,label = "Momento medio")
plt.legend()
plt.plot(x,MM_alt, label = "Momento alternado")
plt.legend()
plt.plot(x,MM_g2, label = "Momento caso 2" )
plt.legend()
##plt.plot(x,MM_g2)
plt.xlabel("Comprimento do eixo (m)")
plt.ylabel("Módulo do momento fletor (Nm)")
plt.show()
plt.savefig('caso_2.png')


raio_escalonamento = 0.01



indice_a = np.where(x > 0.14)[0][0]
indice_b = np.where(x > 0.37)[0][0]
indice_c = np.where(x > 0.43)[0][0]
indice_d = np.where(x > 0.06)[0][0]

indice_g2_a = np.where(x > 0.29)[0][0]
indice_g2_b = np.where(x > 0.37)[0][0]
indice_g2_c = np.where(x > 0.43)[0][0]
indice_g2_d = np.where(x > 0.06)[0][0]



#Convertemos os momentos para lbin
M_a_alt = nm_para_lb_in(MM_alternado[indice_a])
M_b_alt = nm_para_lb_in(MM_alternado[indice_b])
M_c_alt = nm_para_lb_in(MM_alternado[indice_c])
M_d_alt = nm_para_lb_in(MM_alternado[indice_d])

M_a_med = nm_para_lb_in(MM_medio[indice_a])
M_b_med = nm_para_lb_in(MM_medio[indice_b])
M_c_med = nm_para_lb_in(MM_medio[indice_c])
M_d_med = nm_para_lb_in(MM_medio[indice_d])

M_g2_a = nm_para_lb_in(MM_g2[indice_g2_a])
M_g2_b = nm_para_lb_in(MM_g2[indice_g2_b])
M_g2_c = nm_para_lb_in(MM_g2[indice_g2_c])
M_g2_d = nm_para_lb_in(MM_g2[indice_g2_d])

Ta = (T_max-T_min)/2
Tm = (T_max+T_min)/2

delta = 0.2
D2 = 0.5
D1 = D2 - delta
D3 = D2 + delta


D4 = D3 - delta # Precisa sair da parte B

D5 = 0.3
D5_g2 = 0.3
D6_g2 = 0.3
D6 = 0.2
D1 = 0.2

pos_D4 = L1 + L2 + L3 + L4
pos_D5 = pos_D4
indice_D5 = np.where(x > pos_D5)[0][0]
Miumentu = nm_para_lb_in(MM_alternado[indice_D5])
Miumentu2 = nm_para_lb_in(MM_medio[indice_D5])

for i in range(0,1,20):
    D1 = diametro_torsao_variavel(M_a_med, M_a_alt,Ta,Tm, Sut,N,raio_escalonamento,D1, D2, 0)
    D2 = diametro_torsao_variavel(M_a_med, M_a_alt,Ta,Tm, Sut,N,raio_escalonamento,D2, D3, 1)
    D5 = diametro_torsao_variavel(M_b_med, M_b_alt,Ta, Tm, Sut,N,raio_escalonamento, D5, D4,0)
    D6 = diametro_torsao_variavel(M_c_med, M_c_alt,Ta, Tm ,Sut,N,raio_escalonamento,D6, D5,0)
    D4 = diametro_torsao_constante(M_g2_a,Sut, T_g2, Sy,N, D4,0,1) 
    D5_g2 = diametro_torsao_constante(M_g2_b,Sut, T_g2, Sy,N,D5_g2, 0,0)
    D6_g2 = diametro_torsao_constante(M_g2_c,Sut, T_g2, Sy,N,D6_g2, 0,0)


print("D1 ", in_para_mm(D1))
print("D2 ", in_para_mm(D2))
print("D3 ", in_para_mm(D3))
print("D4 ", in_para_mm(D4))
print("D5 ", in_para_mm(D5))
print("D5_g2", in_para_mm(D5_g2))
print("D6 ", in_para_mm(D6))
print("D6_g2", in_para_mm(D6_g2))


Sut_chaveta = 53*1000 # psi
Sy_chaveta = 44*1000 # psi

N_chaveta = 1.5
r_chaveta = D2/2
r_chaveta_g2 = D4/2

Fa = Ta/r_chaveta
Fm = Tm/r_chaveta

#TODO Verificar se a força alternada e o torque alternado g2 são zero
Fa_g2 = 0
Fm_g2 = T_g2/r_chaveta

comprimento_chaveta = 0.6
comprimento_chaveta_g2 = 0.6

N_fadiga_chaveta = 0
N_fadiga_chaveta_g2 = 0
largura_chaveta = calcular_largura_chaveta(D2)
largura_chaveta_g2 = calcular_largura_chaveta(D4)
## incrementamos o valor de passo no comprimento da chaveta até chegar no N desejado
passo = 0.001
while N_fadiga_chaveta < N_chaveta:

    tau_a = Fa/(comprimento_chaveta*largura_chaveta)
    tau_m = Fm/(comprimento_chaveta*largura_chaveta)

    sigma_a = math.sqrt(3*(tau_a)**2)
    sigma_m = math.sqrt(3*(tau_m)**2)

    N_fadiga_chaveta= 1/(sigma_a/Se_corrigir(Sut_chaveta,D2)+ sigma_m/(Sut_chaveta))
    comprimento_chaveta = comprimento_chaveta + passo

while N_fadiga_chaveta_g2 < N_chaveta:

    tau_a_g2 = Fa_g2/(comprimento_chaveta_g2*largura_chaveta_g2)
    tau_m_g2 = Fm_g2/(comprimento_chaveta*largura_chaveta_g2)

    sigma_a_g2 = math.sqrt(3*(tau_a_g2)**2)
    sigma_m_g2 = math.sqrt(3*(tau_m_g2)**2)

    N_fadiga_chaveta_g2 = 1/(sigma_a/Se_corrigir(Sut_chaveta,D2)+ sigma_m/(Sut_chaveta))
    comprimento_chaveta_g2 = comprimento_chaveta_g2 + passo


A_esm = comprimento_chaveta*largura_chaveta/2
sigma_esmagamento = (Fm + Fa)/A_esm
N_esmagamento_chaveta = Sy_chaveta/sigma_esmagamento


A_esm_g2 = comprimento_chaveta_g2*largura_chaveta_g2/2
sigma_esmagamento_g2 = (Fm_g2 + Fa_g2)/A_esm_g2
N_esmagamento_chaveta_g2 = Sy_chaveta/sigma_esmagamento_g2

print("N_esmag", N_esmagamento_chaveta)
print("N_esmag_g2", N_esmagamento_chaveta_g2)
print("N_fadiga", N_fadiga_chaveta)
print("N_fadiga_g2", N_fadiga_chaveta_g2)
print("Comprimento da chaveta", comprimento_chaveta)
print("Comprimento da chaveta_g2", comprimento_chaveta_g2)

# TODO: No calculo de A_esm verificar se pode deixar a chaveta quadrada
# TODO: Ver com o Hélio se um escalonamento de 10% é muito ou pouco

print("#########################")
print("######   MANCAIS   ######")
print("#########################")

N_mh = 3

def modulo(vetor):
    return math.sqrt(vetor[0]**2 + vetor[1]**2 + vetor[2]**2)

print('R2_min', modulo(R2_min))
print('R2_max',modulo(R2_max))
print('R2_g2', modulo(R2_g2))


# TODO: Descobrir de onde o livro tirou esses valores
P = modulo(R2_max)
razao_folga = 0.0017
l_d = 0.5 # TODO: ver se esse valor


Temp = 158 #F

v_max_in = v_max*39.3701

cd = razao_folga*D5
cr = cd/2

l_mancal = l_d*D5
Ocvirk = 20
for i in range(0,1,100):
    e_x = 0.21394 + 0.38517*math.log10(Ocvirk) - 0.0008*(Ocvirk-60)
    K_e = Ocvirk/(4*math.pi)
    viscosidade = (P)*cr*cr/(K_e*v_max_in*(l_mancal**3))
    p_media = P/(l_mancal*D5)
    theta_max = math.acos((1-math.sqrt(1 + 24*e_x**2))/(4*e_x))
    phi = math.atan((math.pi*math.sqrt(1 - e_x**2))/(4*e_x))
    p = (viscosidade*v_max_in)/((D5/2)*cr*cr)*((l_mancal**2)/4 - 0 )*3*e_x*math.sin(theta_max)/((1 + e_x*math.cos(theta_max))**3)
    n = v_max_in/(math.pi*D5)

    Ts = (viscosidade*(D5**3)*l_mancal*(n - 0)*math.pi**2)/(cd*math.sqrt(1-e_x**2))
    Tr = Ts + P*e_x*math.sin(phi)
    Potencia_mancal = 2*math.pi*Tr*(n -0) #in lb / s
    mi = 2*Tr/(P*D5)

    h_min = cr*(1-e_x)
    Ocvirk = (p_media/(viscosidade*n))*(D5/l_mancal)*(D5/l_mancal)*(cd/D5)*(cd/D5)

print("Ocvirk: ",Ocvirk)
print("R1 max",modulo(R1_max_N))
print("R1 min",modulo(R1_min_N))
print("R2 max",modulo(R2_max_N))
print("R2 min",modulo(R2_min_N))
print("R2 alt",lb_para_N(modulo(R2_alt)))
print("R2 med",lb_para_N(modulo(R2_med)))
