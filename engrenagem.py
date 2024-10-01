import math

diametro_primitivo_g1 = 150/25.4 #in
diametro_primitivo_g2 = 200/25.4 #in
diametro_polia = 100

n_dentes_p1 = 38
n_dentes_p2 = 27

E = 190*(10**9) #Pascal
coeficiente_poisson = 0.27

T = 180 # Graus
mv = 0.95
mg1 = 1/mv

v = 1.73
w = v/(diametro_polia/2)
Potencia = 10*6600
Torque = Potencia/w

angulo_pressao = 20
n_dentes_g1 = mg1*n_dentes_p1

passo_diametral_g1 = n_dentes_g1/diametro_primitivo_g1

modulo_g1 = 1/passo_diametral_g1

adendo_g1 = 1/passo_diametral_g1


dedendo_g1 = 1.25/passo_diametral_g1

profundidade_total_g1 = 2.250/passo_diametral_g1

folga_g1 = dedendo_g1 - adendo_g1

diametro_primitivo_p1 = n_dentes_g1/passo_diametral_g1

C_g1 = (diametro_primitivo_g1 + diametro_primitivo_p1)/2

diametro_primitivo_p2 = (C_g1 - diametro_primitivo_g2/2)*2

m_g2 = diametro_primitivo_g2/diametro_primitivo_p2

w_p2 = m_g2*w

n_dentes_g2 = m_g2*n_dentes_p2

passo_diametral_g2 = n_dentes_g2/diametro_primitivo_g2

modulo_g2 = 1/passo_diametral_g2

adendo_g2 = 1/passo_diametral_g2

dedendo_g2 = 1.25/passo_diametral_g2

profundidade_total_g2 = 2.250/passo_diametral_g2

folga_g2 = dedendo_g2 - adendo_g2

diametro_externo_g1 = diametro_primitivo_g1 + 2*adendo_g1
diametro_externo_g2 = diametro_primitivo_g2 + 2*adendo_g1

distancia_centros_g1 = (diametro_primitivo_g1 + diametro_primitivo_p1)/2
distancia_centros_g2 = (diametro_primitivo_g2 + diametro_primitivo_p2)/2

passo_diametral_p1 = n_dentes_p1/diametro_primitivo_p1
modulo_p1 = 1/passo_diametral_p1
adendo_p1 = modulo_p1
dedendo_p1 = 1.25/passo_diametral_p1


passo_diametral_p2 = n_dentes_p2/diametro_primitivo_p2
modulo_p2 = 1/passo_diametral_p2
adendo_p2 = modulo_p2
dedendo_p2 = 1.25/passo_diametral_p2

r_p1 = diametro_primitivo_p1/2
r_g1 = diametro_externo_g1/2
Z = math.sqrt((r_p1+adendo_p1)^2- (r_p1*math.cos(math.radians(angulo_pressao)))^2) + math.sqrt((r_g1+adendo_g1)^2 - (r_g1*math.cos(math.radians(angulo_pressao)))^2) - C_g1*math.sin(math.radians(angulo_pressao))

pc_g1 = math.pi*diametro_primitivo_g1/n_dentes_g1
pb_g1 = pc_g1*math.cos(math.radians(angulo_pressao))
razao_contato_g1 = Z/pb_g1


r_p2 = diametro_primitivo_p1/2
r_g2 = diametro_externo_g1/2
Z = math.sqrt((r_p2+adendo_p2)^2 - (r_p2*math.cos(math.radians(angulo_pressao)))^2) + math.sqrt((r_g2+adendo_g1)^2 - (r_g2*math.cos(math.radians(angulo_pressao)))^2) - C_g1*math.sin(math.radians(angulo_pressao))

pc_g2 = math.pi*diametro_primitivo_g2/n_dentes_g2
pb_g2 = pc_g2*math.cos(math.radians(angulo_pressao))
razao_contato_g2 = Z/pb_g2

velocidade_tangencial_g1 = w*diametro_primitivo_g1/2
velocidade_tangencial_g2 = w*diametro_primitivo_g2/2

forca_tangencial_p1 = Torque/r_p1
forca_tangencial_p2 = Torque/r_p2

face_g1 = forca_tangencial_p1/math.cos(math.radians(angulo_pressao))
face_g2 = forca_tangencial_p1/math.cos(math.radians(angulo_pressao))

#Todo: encontrar o índice de qualidade


#Usamos o fator geométrico de flexão da tabela 12-8 porque é mais seguro.
J_g1 = 0.26
#Todo: verificar com o professor o que fazer se o J está zero para a combinação engrenagem
#pinhão
J_g2 = 0.28