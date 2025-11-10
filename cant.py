F = 10
L = 1
E = 210000000000
I = 78539816.34/1000000000000
delta = F*(L**3)/(3*E*I)
print(I)
print(f"delta = {delta}")
sigma = E*delta
print(f"sigma = {sigma}")

