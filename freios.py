import math

print("Freio sapata curta")

fator_servico = 2

Potencia = 10*736

v1 = 2
v2 = 1.73
r_polia = (100/2)/1000

torque_1= Potencia/(v1/r_polia)
torque_2 = Potencia/(v2/r_polia)

torque_nominal_1 = fator_servico*torque_1
torque_nominal_2 = fator_servico*torque_2


a = 268/1000
b = 153/1000
c = 27/1000

# Todo: Ver se esse coeficiênte de atrito está certo
mi = 0.65
r = 125/1000

razao_auto_energizante = a/(b-mi*c)
#Fn = torque_nominal_2/(mi*r)
theta = 45*math.pi/180

# Tabela 17 - 1
p_max = 690*1000

w = 0.08
Fn = p_max*r*w*theta

print(f"Fator nominal de serviço: {fator_servico:.2f}")
print(f"Comprimento angular da sapata: {theta:.2f}")
print(f"Raio do tambor: {r:.2f}")
print(f"Largura da sapata: {w:.2f}")
print(f"Força Normal: {Fn:.2f}")

Ff = Fn*mi

print(f"Força de atrito: {Ff:.2f}")

Fa = Fn/razao_auto_energizante
print(f"Força de aplicação: {Fn:.2f}")

Tf = Ff*r

print(f"Torque de frenagem máximo atingido pelo freio: {Tf:.2f}")

Rx = -1*Ff
print(f"Reação X no ponto O: {Rx:.2f}")

Ry = Fa - Fn
print(f"Reação Y no ponto O: {Ry:.2f}")

F_pino = math.sqrt(Rx**2 + Ry**2)

Sy = 303*(10**6)

N_pino = 2

diametro_pino = math.sqrt(4*F_pino*N_pino/(math.pi*Sy))
print(f"Diâmetro do pino: {diametro_pino}")