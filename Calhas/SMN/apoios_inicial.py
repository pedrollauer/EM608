from Pynite import FEModel3D
import pprint
import math as math
from rich.console import Console
from rich.table import Table



def print_beam(apoios, comprimento):
    scale = 20

    padding = 3
    beam="   "
    supports ="   "
    dimensions =""
    apoios_m = 1000*apoios 
    l = 0
    num_segs = int(comprimento/scale)

    for i in range(0, padding):
        print("")

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
    
    for i in range(0, padding):
        print("")

def encontrar_apoios():
    return None

print(" === APOIOS 0.01 ===")
print(" ^                 ^")

### Configurações
Rr = 1.5

resolucao = 10
L = 1000
tents = L/1000
### 

beam = FEModel3D()




apoios = [70/1000, 766/1000]
print(" === GEOMETRIA ===")
print()

print_beam(apoios, 1000)

beam.add_node('N1', 0, 0, 0)
beam.add_node('N2', apoios[0], 0, 0)
beam.add_node('N3', apoios[1], 0, 0)
beam.add_node('N4', 1, 0, 0)

E = 193e9       
nu = 0.29
G = E/(2*(nu+1))       
rho = 8000

Ix =  36702.655# mm4
Iy =  88743.085
A =  1106.66    # mm2 
J = Ix + Iy

L = L/1000
Iy = Iy/(1000**(4))
Ix = Ix/(1000**(4))
A = A/(1000**2)


F_prova = -1000


beam.add_material('Steel', E, G, nu, rho)
beam.add_section('MySection',A , Iy, Ix, J)

# CRIAR MEMBROS
beam.add_member('M1', 'N1', 'N2', 'Steel', 'MySection')
beam.add_member('M2', 'N2', 'N3', 'Steel', 'MySection')
beam.add_member('M3', 'N3', 'N4', 'Steel', 'MySection')

# 
beam.def_support('N2', True, True, True, False, False, False)
beam.def_support('N3', True, True, True, False, False, False)

beam.add_node_load('N4', "FY", F_prova, case = 'D')
beam.add_load_combo('D', factors={'D': 1.0})
beam.analyze()



Vol = A*L
max_def = abs(beam.members['M3'].max_deflection('dy','D'))
min_def = abs(beam.members['M3'].min_deflection('dy','D'))

def_prova = max(max_def, min_def)

k_beam =abs(F_prova/def_prova)
massa = Vol*rho



table = Table(title="Resultados", show_lines=True, safe_box=True, show_header=False)

table.add_column("Parâmetro", justify="right", no_wrap=True)
table.add_column("Valor", justify="right", no_wrap=True)
table.add_column("Unidade", justify="right", no_wrap=True)

table.add_row("Rigidez Calha",f"{k_beam : .2f}"," [N/m]")
table.add_row("Deflexao",f"{def_prova*1000:.2f} "," mm")
table.add_row("Massa",f"{massa:.2f} ","kg")

console = Console()
console.print(table)

print()
print()
