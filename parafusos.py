import math
espessura_mancal = 20 #mm
espessura_base = 45 #mm

E = 200*10**9/6895 

P_max = 10000*0.2248

At_uns = 0.0775
At_iso = 57,99/645.2

l = (20+45)/25.4
lb_uns = l + 1/2 
lb_iso = l + 1/2 
print(f"Comprimento parafuso UNS {lb_uns} in")
print(f"Comprimento parafuso UNS {lb_iso} in")

d_uns = 3/8
d_iso = 10/25.4
lt_uns = 2*d_uns+1/4#
lt_iso = 2*d_iso+1/4

print(f"Comprimento rosqueado UNS {lt_uns} in")
print(f"Comprimento rosqueado ISO {lt_uns} in")

ls_uns = lb_uns - lt_uns
ls_iso = lb_iso - lt_iso

lt_junta_uns = l - ls_uns
lt_junta_iso = l - ls_iso

print(f"Comprimento rosqueado sob tração UNS {lt_junta_uns} in")
print(f"Comprimento rosqueado sob tração ISO {lt_junta_iso} in")

phi = 40/180*math.pi

d2_uns = 2*d_uns
d2_iso = 2*d_iso

Ab_uns = math.pi*(d_uns**2)/4
Ab_iso = math.pi*(d_iso**2)/4

d3_uns = d2_uns + l*math.tan(phi)
d3_iso = d2_iso + l*math.tan(phi)

Deff_uns = (d2_uns + d3_uns)/2
Deff_iso = (d2_iso + d3_iso)/2

Am_uns = math.pi*(Deff_uns**2-d_uns**2)/4
Am_iso = math.pi*(Deff_iso**2-d_iso**2)/4

print(f"Área efetiva em esmagamento na junta UNS {Am_uns} in")
print(f"Área efetiva em esmagamento na junta ISO {Am_iso} in")


kb_uns = (lt_junta_uns/(At_uns*E)+(l-lt_junta_uns)/(Ab_uns*E))^-1
kb_iso = (lt_junta_iso/(At_iso*E)+(l-lt_junta_iso)/(Ab_iso*E))^-1

print(f"Constante de rigidez do parafuso UNS {kb_uns} in")
print(f"Constante de rigidez do parafuso ISO {kb_iso} in")

km_uns = Am_uns*E/l
km_iso = Am_iso*E/l

print(f"Constante de rigidez da junta UNS {km_uns} in")
print(f"Constante de rigidez da junta ISO {km_iso} in")

cj_uns = kb_uns/(kb_uns+km_uns)
cj_iso = kb_iso/(kb_iso+km_iso)

print(f"Constante da junta UNS {cj_uns} in")
print(f"Constante da junta ISO {cj_iso} in")


resistencia_prova_uns = 85*1000
resistencia_prova_iso = 310*10**6/6895

Np_uns = 0.75*resistencia_prova_uns
Np_iso = 0.75*resistencia_prova_iso

print(f"Pré carga junta UNS {Np_uns} in")
print(f"Pré carga junta ISO {Np_iso} in")

Pb_uns = cj_uns*P_max
Pb_iso = cj_iso*P_max

print(f"Força resultante no parafuso UNS {Pb_uns} in")
print(f"Força resultante no parafuso ISO {Pb_ijuntaso} in")

Pm_uns = (1-cj_uns)*P_max
Pm_iso = (1-cj_iso)*P_max

print(f"Força resultante na junta UNS {Pm_uns} in")
print(f"Força resultante na junta ISO {Pm_iso} in")

Fi_uns = Np_uns/At_uns
Fi_iso = Np_iso/At_iso


Nsep_uns = Fi_uns/((1-cj_uns)*P_max)
Nsep_iso = Fi_iso/((1-cj_iso)*P_max)

print(f"Coeficiente de segurança de separação na junta UNS {Nsep_uns} in")
print(f"Coeficiente de segurança de separação na junta ISO {Nsep_iso} in")



















