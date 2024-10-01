# Molas
# Material ASTM A232 (cromo vanádio)

import math
print('EM608 - Parte 3')

g = 9.81
m = 410
F_min = 410*9.8
F_max = 3000 + F_min

k_eq_min = 310
d = 6/1000
C = 4

# Todo: Ajustar o chute inicial de número de molas

n = 5
print(f"Número de molas: {n}")

D = C*d
print(f"Diâmetro médio da espira: {D}")

Ks = 1 + 0.5/C
print(f"Fator de cisalhamento {Ks}")

Kw = (4*C - 1)/(4*C-4) + 0.615/C
print(f"Fator de Wahl {Kw}")

Sut = ((1909.9)*pow(d, -0.1453))*(10**6)
print(f"Resistência à tração: {Sut}")

Sus = 0.67*Sut
print(f"Resistência à torção: {Sus}")

Sys = 0.75*Sut
print(f"Resistência ao escoamento por torção: {Sys}")

num_ciclos = 27*10**7

Sfw = 0.46*Sut
print(f"Resistência  à fadiga torcional: {Sfw}")

Sew = 465*10**6
print(f"Limite de resist. à fadiga torcional: {Sew}")

Ses = 0.5*(Sew*Sus)/(Sus-0.5*Sew)
print(f"Resist. à fadiga sob carga alternada: {Ses}")


F_min_mola = F_min/n
print(f"Força mínima por mola: {F_min_mola}")

F_max_mola = F_max/n
print(f"Força máxima por mola: {F_max_mola}")

F_media_mola = 0.5*(F_min_mola + F_max_mola)
print(f"Força média por mola: {F_media_mola}")

F_alternada_mola = 0.5*(F_max_mola - F_min_mola )
print(f"Força alternada por mola: {F_alternada_mola}")

tau_i = Ks*(8*F_min_mola*D)/(math.pi*(d**3))
print(f"Tensão de cisalhamento inicial: {tau_i}")


tau_m = Ks*(8*F_media_mola*D)/(math.pi*(d**3))
print(f"Tensão de cisalhamento média: {tau_m}")

tau_a = Ks*(8*F_alternada_mola*D)/(math.pi*(d**3))
print(f"Tensão de cisalhamento alternada: {tau_a}")

Nfs = Ses*(Sus-tau_i)/(Ses*(tau_m-tau_i) + Sus*tau_a)
print(f"Coeficiênte de segurança de fadiga: {Nfs}")

G = 11.56*10**6*6895
keq = 310*10**3
k = keq/n

Na = ((d**4)*G)/(8*(D**3)*k)
Na =round(Na*4)/4

k = (d**4)*G/(8*(D**3)*Na)

Na = ((d**4)*G)/(8*(D**3)*k)
print(f"Número de espiras ativas: {Na}")

# Todo: Verificar se precisa mudar o tipo de mola
Nt = Na + 1
print(f"Número total de espiras: {Na}")

print(f"Rigidez corrigida de cada mola: {k}")

y_inicial = F_min_mola/k
print(f"Deflexão inicial corrigida: {y_inicial}")

keq = n*k
print(f"Rigidez equivalente corrigida: {keq}")


Ls = d*Nt
print(f"Comprimento fechado da mola: {Ls}")

y_interf = 0.15*y_inicial
print(f"Tolerância de contato (15%): {y_interf}")

y_trab = (F_max_mola - F_min_mola)/k
print(f"Deflexão de trabalho: {y_trab}")

Lf = Ls + y_interf + y_trab + y_inicial
print(f"Comprimento livre: {Lf}")

# y_fechado = Lfechado(Lf)
Lfech = Lf - Ls
print(f"Deflexão para fechar mola: {Lfech}")

F_fech = k*Lfech
print(f"Força para fechar mola: {F_fech}")

tau_fechada = Ks*(8*F_fech*(D))/(math.pi*(d**3))
print(f"Tensão de fechamento da mola: {tau_fechada}")


N_fech = Sys/tau_fechada
print(f"Fator de segurança defechamento: {N_fech}")

gama = 78*1000

# Todo: revisar o valor
Wa = (math.pi**2)*(d**2)*(D)*Na*gama/4
print(f"Peso das espiras ativas da mola: {Wa}")

m_mola =(1/g)*(math.pi**2)*(d**2)*(D)*Nt*gama/4
print(f"Massa de cada mola: {m_mola}")

fn_sistema = math.sqrt(n*k/410)
fn = math.sqrt(k*g/Wa)
Rw = fn/fn_sistema
print(f"Razão de frequências: {Rw}")

LfD = Lf/D
print(f"Razão 𝐿𝑓 /𝐷: {LfD}")

y_max = y_inicial+y_trab
y_maxLf = y_max/Lf
print(f"Razão 𝑦𝑚á𝑥/𝐿𝑓: {y_maxLf}")
