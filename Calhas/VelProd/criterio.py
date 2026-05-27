import math as mt

F = 1000
d = 0.2/1000

k = F/d

Lm = (80-16.5)/1000
a = 47/1000
L = (47/1000)/2
h = 2.79/1000
E = 23e9
W = 65/1000

I = (900/2)*(W*h**3)/1002

kma =(3*E*I/(L**3))

crit = k/kma

dc = 1000/kma
print(f"d_crit: {dc}")

if(crit < 0.94):
    print(f"crt > {crit:.2f}")
    print("Perigoso.")

if(crit > 0.94):
    print(f"crt < {crit:.2f}")
    print("Ok")
