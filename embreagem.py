import math


fator_servico = 2.8

v1 = 2
v2 = 1.73
r_polia = (100/2)/1000

Potencia = 10*736
torque_1= Potencia/(v1/r_polia)
torque_2 = Potencia/(v2/r_polia)

torque_nominal_1 = fator_servico*torque_1
torque_nominal_2 = fator_servico*torque_2

mi = 0.65
p_max = 2.48*(10**6)

r_o_1 = math.pow(torque_1/(0.3849*math.pi*mi*p_max),1/3)
r_i_1 = r_o_1/(math.sqrt(3))
r_i_1 = round(1000*r_i_1)/1000

r_o_2 = math.pow(torque_2/(0.3849*math.pi*mi*p_max),1/3)
r_i_2 = r_o_2/(math.sqrt(3))
r_i_2 = round(1000*r_i_2)/1000
print(f"Torque nominal de projeto 1: {torque_nominal_1:.2f}")
print(f"Torque nominal de projeto 2: {torque_nominal_2:.2f}")


print("====== DESGASTE UNIFORME ======")
print(f"Raio externo 1: {r_o_1:.4f}")
print(f"Raio interno 1: {r_i_1:.4f}")

print(f"Raio externo 2: {r_o_2:.4f}")
print(f"Raio interno 2: {r_i_2:.4f}")

f_axial_1 = 2*math.pi*r_i_1*p_max*(r_o_1-r_i_1)
f_axial_2 = 2*math.pi*r_i_1*p_max*(r_o_2-r_i_2)
print(f"Força exercida pela embreagem 1: {f_axial_1:.2f}")
print(f"Força exercida pela embreagem 2: {f_axial_2:.2f}")

r_o_1 = r_i_1*(math.sqrt(3))
torque_1_r = (r_o_1**3)*0.3849*math.pi*mi*p_max
fator_servico_1 = torque_nominal_1/torque_1_r


r_o_2 = r_i_2*(math.sqrt(3))
torque_2_r = (r_o_2**3)*0.3849*math.pi*mi*p_max
fator_servico_2 = torque_nominal_2/torque_2_r

print(f"Fator de serviço final: {fator_servico_1}")
print(f"Fator de serviço final 2: {fator_servico_2}")


print("====== PRESSÃO UNIFORME ======")

#Todo: Verificar
N = 1
r_o_1_p = math.pow((3*torque_nominal_1/(2*math.pi*p_max*mi))*math.pow(1-1/(math.sqrt(3)**3),-1),1/3)

r_i_1_p = r_o_1_p/math.sqrt(3)

F_1_p = p_max*math.pi*(r_o_1_p**2 - r_i_1_p**2)

r_o_2_p = math.pow((3*torque_nominal_2/(2*math.pi*p_max*mi))*math.pow(1-1/(math.sqrt(3)**3),-1),1/3)

r_i_2_p = r_o_2_p/math.sqrt(3)

F_2_p = p_max*math.pi*(r_o_2_p**2 - r_i_2_p**2)


r_i_1_p = round(1000*r_i_1_p)/1000
print(f"Raio interno: {r_i_1_p}")

r_i_2_p = round(1000*r_i_2_p)/1000
print(f"Raio interno 2: {r_i_2_p}")

r_o_1_p = round(1000*r_o_1_p)/1000
print(f"Raio externo: {r_o_1_p}")

r_o_2_p = round(1000*r_o_2_p)/1000
print(f"Raio externo 2: {r_o_2_p}")

print(f"Força exercida pela embreagem 1: {F_1_p:.2f}")
print(f"Força exercida pela embreagem 2: {F_2_p:.2f}")

torque_1_r_p = 2*math.pi*p_max*mi*(r_o_1**3-r_i_1**3)*N/3
fator_servico = torque_nominal_1/torque_1_r_p
print(f"Fator de serviço final: {fator_servico}")


torque_2_r_p = 2*math.pi*p_max*mi*(r_o_2**3-r_i_2**3)*N/3
fator_servico_2 = torque_nominal_2/torque_2_r_p
print(f"Fator de serviço final: {fator_servico_2}")