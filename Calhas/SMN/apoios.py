from Pynite import FEModel3D
import pprint
import math as math


def print_beam(apoios, comprimento):
    scale = 20

    padding = 3
    beam="   "
    supports ="   "
    dimensions =""
    apoios_m = 1000*apoios 
    l = 0
    num_segs = int(comprimento/scale)
    for i in range(0, num_segs):
        beam = beam + '='

    j = 0
    num_chars = []

    for i in range(0, num_segs):
        l = i*scale

        if(j < len(apoios) and l>=1000*apoios[j]):
            
            j = j + 1
            supports = supports + "^"
            num_chars.append(i+padding)
            if j  >= len(apoios):
               continue 
        else:
            supports = supports + " "
        
    dimensions = list(supports)
    j = 0 
    for k in num_chars:
        dimensions[k] = "|"
        dim = " " + str(int(1000*apoios[j]))

        for i in range(len(dim)):
            dimensions[k+i+1] = dim[i]

        j = j + 1

    
    dimensions[padding] = "|"
    dimensions[1+padding] = "0"
    dimensions = "".join(dimensions)

    print(beam)
    print(supports)
    print(dimensions)

def encontrar_apoios():
    return None
beam = FEModel3D()

# o primeiro é o começo da calha
# o último o fim
# 
apoios = [70/1000, 470/1000, 600/1000]
print_beam(apoios, 1000)

beam.add_node('N1', apoios[0], 0, 0)
beam.add_node('N2', apoios[1], 0, 0)
beam.add_node('N3', 1000, 0, 0)

E = 29e9       
nu = 0.30
G = E/(2*(nu+1))       
nu = 0.3        
rho = 7850 

Iy = 6021051.44 # mm4
Ix = 146810.62  # mm4
A =  1106.66    # mm2 

Iy = Iy/(1000**(4))
Ix = Ix/(1000**(4))
A = A/(1000**2)

J = math.sqrt(Ix*Ix + Iy*Iy)
beam.add_material('Steel', E, G, nu, rho)
beam.add_section('MySection',A , Iy, Ix, J)
beam.add_member('M1', 'N1', 'N2', 'Steel', 'MySection')
beam.add_member('M2', 'N2', 'N3', 'Steel', 'MySection')
beam.def_support('N1', True, True, True, False, False, False)
beam.def_support('N2', True, True, True, True, False, False)

#beam.add_member_dist_load('M2', 'Fy', -200/1000/12, -200/1000/12, 0, apoios[0],case='D')
beam.add_member_pt_load('M1', 'Fy', -5000, 0, 'D')
beam.add_load_combo('D', factors={'D': 1.0})
beam.analyze()
#beam.members['M1'].plot_deflection('dy', 'D')

print(beam.members['M1'].max_deflection('dy','D'))
print(beam.members['M1'].min_deflection('dy','D'))

beam.add_load_combo('Mass', {'D': 1.0})

                            


print(f"Left Support Reaction: { {k: float(v) for k, v in beam.nodes['N1'].RxnFY.items()} }")
print(f"Right Support Reaction: { {k: float(v) for k, v in beam.nodes['N2'].RxnFY.items()} }")

