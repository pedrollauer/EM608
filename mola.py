import math as m

nu = 0.28
E = 210*10**9
D = 11/1000
d = 2/1000
Nt = 7
G = E/(2*(nu+1))

Na = Nt-1
ki = (d**4)*G/(8*(D**3)*Na)

df = 3/1000
kf = (df**4)*G/(8*(D**3)*Na)

q = kf/ki
print(f"Coeficiente inicial: {ki}")
print(f"Coeficiente novo: {kf}")
print(f"Razão: {q}")

F = 9.8*1
delta_i = F/ki
delta_f = F/kf
qd = delta_f/delta_i

print(f"delta_i: {delta_i}")
print(f"delta_f: {delta_f}")
print(f"Razão: {qd}")
