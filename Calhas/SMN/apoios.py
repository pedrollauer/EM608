from Pynite import FEModel3D
import pprint
import math as math
from rich.console import Console
from rich.table import Table

_debug = False
_parar = False

def _print(texto:str=""):
    if _debug:
        print(texto)

    

def print_beam(apoios, comprimento):
    scale = 20

    padding = 3
    beam="   "
    supports ="   "
    dimensions =""

    l = 0
    num_segs = int(comprimento/scale) + 1


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
        
        if k + len(dim) > len(dimensions):
            dimensions+=[0]*(len(dim))

        for i in range(0, len(dim)):
            dimensions[k+i+1] = dim[i]

        j = j + 1

    
    dimensions[padding] = "|"
    dimensions[1+padding] = "0"
    dimensions = "".join(dimensions)
    
    plot = "\033[11A"
    plot += '\033[K' + " === GEOMETRIA ===" + '\n'
    plot += '\033[K' + '\n' + '\033[K' + '\n' + '\033[K'+'\n'  
    plot += '\033[K' + beam + '\n'
    plot += '\033[K' + supports + '\n' 
    plot += '\033[K' + dimensions + '\n'
    plot += '\033[K' +'\n' + '\033[K' +'\n' + '\033[K' +'\n'
    plot += '\033[K' + '\n'

    # print(plot, end="", flush=True)

    

def encontrar_apoios():
    return None

print(" === APOIOS 0.01 ===")
print(" ^                 ^")

### Configurações
Rr = 1.5

resolucao = 10
L = 1000
tents = int(L/resolucao)
num_min_apoios = 2
num_max_apoios = 4
### 

k_mola = 555683.4678
L = L /1000


E = 193e9       
nu = 0.29
G = E/(2*(nu+1))       
rho = 8000

Ix =  36702.655# mm4
Iy =  88743.085
A =  1106.66    # mm2 
J = Ix + Iy

Iy = Iy/(1000**(4))
Ix = Ix/(1000**(4))
A = A/(1000**2)


F_prova = -1000
k_max = 0
defl_min = 0
c_apoios_ideal = []

print('\n'*11)
for i in range(num_min_apoios, num_max_apoios):
    
    apoios = []
    opc = 0

    for j in range(1, i*tents):
        beam = FEModel3D()
        
        if(j < 91 and i == 2):
         apoios = [0, 10*j/(L*1000)]
        if j >= 91 and i == 2:
         apoios = [(j-90)*10/(L*1000), 0.9 - (j-90)*10/(L*1000) ]

        if(j < 91 and i == 3):
         apoios = [0, 10*j/(L*1000),L]
        if j >= 91 and i == 3:
         apoios = [(j-90)*10/(L*1000),L/2, 0.9 - (j-90)*10/(L*1000) ]

        _print(f"== APOIOS {j} ==")
        _print(apoios)
        _print(f"TAMANHO MALHA: {tents}")
        _print(f"NUMERO APOIOS: {i}")

        # Os apoios estão no mesmo nó
        if(len(apoios) != len(set(apoios))):
            break
        
        print_beam(apoios,1000)
        num_nos = i 
        nos = apoios.copy()
        nos_ponta = []

        # Precisa de nós nas pontas?
        if apoios[0] != 0:
            num_nos = num_nos + 1
            nos.insert(0,0)
            nos_ponta.append(0) # Nó em balanco em 0

        if apoios[len(apoios)-1] != L:
            num_nos = num_nos + 1
            nos.append(L)
            nos_ponta.append(len(nos)-1) # Nó em balanco no fim
        
        
        for k in range(0, len(nos)):
            nome = "N"+str(k)
            beam.add_node(nome, nos[k], 0, 0)
            _print(f"{nome} em {nos[k]}")



        beam.add_material('ACO', E, G, nu, rho)
        beam.add_section('SECCAO_A',A , Iy, Ix, J)

# CRIAR MEMBROS
        num_membros = len(nos)/2

        membros = []
        for k in range(0, len(nos)-1):
            nome = 'M' + str(k)
            n1 = 'N' + str(k)
            n2 = 'N' + str(k+1)
            beam.add_member(nome, n1, n2, 'ACO', 'SECCAO_A')
            membros.append(k)
            _print(f"{nome} com os nós: {n1}, {n2}")

# Colocar apoios
        for k in range(0, num_nos):
            if k in nos_ponta:
                continue
            nome = 'N' + str(k)
            beam.def_support(nome, True, True, True, False, False, False)
            _print(f"APOIO em N{k}")
            _print(nos_ponta)


# Testar deflexao
        # Testamos as pontas e pontos médios entre apoios
        _print(f"PONTA INICIAL:  M{membros[0]}")
        _print(f"PONTA FINAL:  M{membros[len(membros)-1]}")

# Colocar cargas
        x_local = 0
        apoio_local = 0
        _print()

        for k in range(0, len(membros)):
            nome = 'M' + str(k)
            taman = beam.members[nome].L()
            #x_local = x_local + taman

            #Se o membro está bi-apoiado carregamos o centro
            #Se o membro está mono-apoiado carregamos a ponta em balanco

            #ponto de aplicacao da forca
            pt_app = -1
            
            _print(f"APOIO LOCAL: {apoio_local}")
            _print(f"X APOIOS LOCAL: {apoios[apoio_local]}")
            _print(f"X LOCAL: {x_local}")
            _print(f"TAMAN : {taman}")

            if apoio_local == (i-1)  and (taman) != apoios[apoio_local]:
                pt_app = taman-1/10000
                _print(f"{nome} PAPP: {pt_app} NO FIM.")

            elif x_local == apoios[apoio_local]:
                pt_app = taman*0.5 
                _print(f"{nome} F NO MEIO.")

            else: 
                pt_app = 0
                _print(f"{nome} F NO COMECO.")
                apoio_local = apoio_local + 1

            beam.add_member_pt_load(nome, 'FY',F_prova, pt_app,nome)
            beam.add_load_combo(nome, factors={nome: 1.0})

            #x_local = x_local + taman
            _print()

        print(f"RUN: {j}")
        beam.analyze()
        print(f"RUN: {j}")
/home/pedro/venvs/aster311/lib/python3.11/site-packages/Pynite/FEModel3D.py:2437: MatrixRankWarning: Matrix is exactly singular
  Delta_D1 = spsolve(K11, np.subtract(np.subtract(Delta_P1, Delta_FER1), K12 @ Delta_D2))
 === APOIOS 0.01 ===
 ^                 ^












RUN: 1
RUN: 1
RUN: 2
RUN: 2
RUN: 3
RUN: 3
RUN: 4
RUN: 4
RUN: 5
RUN: 5
RUN: 6
RUN: 6
RUN: 7
RUN: 7
RUN: 8
RUN: 8
RUN: 9
RUN: 9
RUN: 10
RUN: 10
RUN: 11
RUN: 11
RUN: 12
RUN: 12
RUN: 13
RUN: 13
RUN: 14
RUN: 14
RUN: 15
RUN: 15
RUN: 16
RUN: 16
RUN: 17
RUN: 17
RUN: 18
RUN: 18
RUN: 19
RUN: 19
RUN: 20
RUN: 20
RUN: 21
RUN: 21
RUN: 22
RUN: 22
RUN: 23
RUN: 23
RUN: 24
RUN: 24
RUN: 25
RUN: 25
RUN: 26
RUN: 26
RUN: 27
RUN: 27
RUN: 28
RUN: 28
RUN: 29
RUN: 29
RUN: 30
RUN: 30
RUN: 31
RUN: 31
RUN: 32
RUN: 32
RUN: 33
RUN: 33
RUN: 34
RUN: 34
RUN: 35
RUN: 35
RUN: 36
RUN: 36
RUN: 37
RUN: 37
RUN: 38
RUN: 38
RUN: 39
RUN: 39
RUN: 40
RUN: 40
RUN: 41
RUN: 41
RUN: 42
RUN: 42
RUN: 43
RUN: 43
RUN: 44
RUN: 44
RUN: 45
RUN: 45
RUN: 46
RUN: 46
RUN: 47
RUN: 47
RUN: 48
RUN: 48
RUN: 49
RUN: 49
RUN: 50
RUN: 50
RUN: 51
RUN: 51
RUN: 52
RUN: 52
RUN: 53
RUN: 53
RUN: 54
RUN: 54
RUN: 55
RUN: 55
RUN: 56
RUN: 56
RUN: 57
RUN: 57
RUN: 58
RUN: 58
RUN: 59
RUN: 59
RUN: 60
RUN: 60
RUN: 61
RUN: 61
RUN: 62
RUN: 62
RUN: 63
RUN: 63
RUN: 64
RUN: 64
RUN: 65
RUN: 65
RUN: 66
RUN: 66
RUN: 67
RUN: 67
RUN: 68
RUN: 68
RUN: 69
RUN: 69
RUN: 70
RUN: 70
RUN: 71
RUN: 71
RUN: 72
RUN: 72
RUN: 73
RUN: 73
RUN: 74
RUN: 74
RUN: 75
RUN: 75
RUN: 76
RUN: 76
RUN: 77
RUN: 77
RUN: 78
RUN: 78
RUN: 79
RUN: 79
RUN: 80
RUN: 80
RUN: 81
RUN: 81
RUN: 82
RUN: 82
RUN: 83
RUN: 83
RUN: 84
RUN: 84
RUN: 85
RUN: 85
RUN: 86
RUN: 86
RUN: 87
RUN: 87
RUN: 88
RUN: 88
RUN: 89
RUN: 89
RUN: 90
RUN: 90
RUN: 91
RUN: 91
RUN: 92
RUN: 92
RUN: 93
RUN: 93
RUN: 94
RUN: 94
RUN: 95
RUN: 95
RUN: 96
RUN: 96
RUN: 97
RUN: 97
RUN: 98
RUN: 98
RUN: 99
RUN: 99
RUN: 100
RUN: 100
RUN: 101
RUN: 101
RUN: 102
RUN: 102
RUN: 103
RUN: 103
RUN: 104
RUN: 104
RUN: 105
RUN: 105
RUN: 106
RUN: 106
RUN: 107
RUN: 107
RUN: 108
RUN: 108
RUN: 109
RUN: 109
RUN: 110
RUN: 110
RUN: 111
RUN: 111
RUN: 112
RUN: 112
RUN: 113
RUN: 113
RUN: 114
RUN: 114
RUN: 115
RUN: 115
RUN: 116
RUN: 116
RUN: 117
RUN: 117
RUN: 118
RUN: 118
RUN: 119
RUN: 119
RUN: 120
RUN: 120
RUN: 121
RUN: 121
RUN: 122
RUN: 122
RUN: 123
RUN: 123
RUN: 124
RUN: 124
RUN: 125
RUN: 125
RUN: 126
RUN: 126
RUN: 127
RUN: 127
RUN: 128
RUN: 128
RUN: 129
RUN: 129
RUN: 130
RUN: 130
RUN: 131
RUN: 131
RUN: 132
RUN: 132
RUN: 133
RUN: 133
RUN: 134
RUN: 134
RUN: 1
RUN: 1
RUN: 2
RUN: 2
RUN: 3
RUN: 3
RUN: 4
RUN: 4
RUN: 5
RUN: 5
RUN: 6
RUN: 6
RUN: 7
RUN: 7
RUN: 8
RUN: 8
RUN: 9
RUN: 9
RUN: 10
RUN: 10
RUN: 11
RUN: 11
RUN: 12
RUN: 12
RUN: 13
RUN: 13
RUN: 14
RUN: 14
RUN: 15
RUN: 15
RUN: 16
RUN: 16
RUN: 17
RUN: 17
RUN: 18
RUN: 18
RUN: 19
RUN: 19
RUN: 20
RUN: 20
RUN: 21
RUN: 21
RUN: 22
RUN: 22
RUN: 23
RUN: 23
RUN: 24
RUN: 24
RUN: 25
RUN: 25
RUN: 26
RUN: 26
RUN: 27
RUN: 27
RUN: 28
RUN: 28
RUN: 29
RUN: 29
RUN: 30
RUN: 30
RUN: 31
RUN: 31
RUN: 32
RUN: 32
RUN: 33
RUN: 33
RUN: 34
RUN: 34
RUN: 35
RUN: 35
RUN: 36
RUN: 36
RUN: 37
RUN: 37
RUN: 38
RUN: 38
RUN: 39
RUN: 39
RUN: 40
RUN: 40
RUN: 41
RUN: 41
RUN: 42
RUN: 42
RUN: 43
RUN: 43
RUN: 44
RUN: 44
RUN: 45
RUN: 45
RUN: 46
RUN: 46
RUN: 47
RUN: 47
RUN: 48
RUN: 48
RUN: 49
RUN: 49
RUN: 50
RUN: 50
RUN: 51
RUN: 51
RUN: 52
RUN: 52
RUN: 53
RUN: 53
RUN: 54
RUN: 54
RUN: 55
RUN: 55
RUN: 56
RUN: 56
RUN: 57
RUN: 57
RUN: 58
RUN: 58
RUN: 59
RUN: 59
RUN: 60
RUN: 60
RUN: 61
RUN: 61
RUN: 62
RUN: 62
RUN: 63
RUN: 63
RUN: 64
RUN: 64
RUN: 65
RUN: 65
RUN: 66
RUN: 66
RUN: 67
RUN: 67
RUN: 68
RUN: 68
RUN: 69
RUN: 69
RUN: 70
RUN: 70
RUN: 71
RUN: 71
RUN: 72
RUN: 72
RUN: 73
RUN: 73
RUN: 74
RUN: 74
RUN: 75
RUN: 75
RUN: 76
RUN: 76
RUN: 77
RUN: 77
RUN: 78
RUN: 78
RUN: 79
RUN: 79
RUN: 80
RUN: 80
RUN: 81
RUN: 81
RUN: 82
RUN: 82
RUN: 83
RUN: 83
RUN: 84
RUN: 84
RUN: 85
RUN: 85
RUN: 86
RUN: 86
RUN: 87
RUN: 87
RUN: 88
RUN: 88
RUN: 89
RUN: 89
RUN: 90
RUN: 90
RUN: 91
RUN: 91
RUN: 92
RUN: 92
RUN: 93
RUN: 93
RUN: 94
RUN: 94
RUN: 95
RUN: 95
RUN: 96
RUN: 96
RUN: 97
RUN: 97
RUN: 98
RUN: 98
RUN: 99
RUN: 99
RUN: 100
RUN: 100
RUN: 101
RUN: 101
RUN: 102
RUN: 102
RUN: 103
RUN: 103
RUN: 104
RUN: 104
RUN: 105
RUN: 105
RUN: 106
RUN: 106
RUN: 107
RUN: 107
RUN: 108
RUN: 108
RUN: 109
RUN: 109
RUN: 110
RUN: 110
RUN: 111
RUN: 111
RUN: 112
RUN: 112
RUN: 113
RUN: 113
RUN: 114
RUN: 114
RUN: 115
RUN: 115
RUN: 116
RUN: 116
RUN: 117
RUN: 117
RUN: 118
RUN: 118
RUN: 119
RUN: 119
RUN: 120
RUN: 120
RUN: 121
RUN: 121
RUN: 122
RUN: 122
RUN: 123
RUN: 123
RUN: 124
RUN: 124
RUN: 125
RUN: 125
RUN: 126
RUN: 126
RUN: 127
RUN: 127
RUN: 128
RUN: 128
RUN: 129
RUN: 129
                Resultados                
┌───────────────┬───────────────┬────────┐
│ RIGIDEZ CALHA │  134486148.71 │  [N/m] │
├───────────────┼───────────────┼────────┤
│      DEFLEXAO │          0.98 │     mm │
├───────────────┼───────────────┼────────┤
│         MASSA │          8.85 │     kg │
└───────────────┴───────────────┴────────┘


        
        # Encontrar a maior deflecção e imprimir para debug
        _print("")
        maxima_defl_local = 0

        for k in membros:
          nome = 'M' + str(k)
          _print(f"MEMBRO: {nome}")
          max_def = abs(beam.members[nome].max_deflection('dy',nome))
          min_def = abs(beam.members[nome].min_deflection('dy',nome))
          def_prova = max(max_def, min_def)
          _print(f"DEFLEXAO MAXIMA:  {max_def}")
          _print(f"DEFLEXAO MINIMA:  {min_def}")
          _print("")

          if(def_prova > maxima_defl_local):
              maxima_defl_local = def_prova

        if(def_prova == 0 or def_prova < 1e-8):
            continue

        k_beam =(-1)*(F_prova/def_prova)

        if math.isfinite(k_beam) and k_max < k_beam:
            k_max = k_beam
            c_apoios_ideal = apoios
            defl_min = maxima_defl_local 

        if(_parar):
            _print(f"MÁXIMA DEFLEXÃO: {maxima_defl_local*1000:.2f} mm")
            _print(f"RIGIDEZ MÍNIMA: {k_beam:.2f} N/m \n")
            opc = input("CONTINUAR ? ")
        if(opc == 'n'):
            break

    if(opc == 'n'):
        break



print_beam(c_apoios_ideal,1000)

Vol = A*L


massa = Vol*rho



table = Table(title="Resultados", show_lines=True, safe_box=True, show_header=False)

table.add_column("Parâmetro", justify="right", no_wrap=True)
table.add_column("Valor", justify="right", no_wrap=True)
table.add_column("Unidade", justify="right", no_wrap=True)

table.add_row("RIGIDEZ CALHA",f"{k_max: .2f}"," [N/m]")
table.add_row("DEFLEXAO",f"{defl_min*1000:.2f} "," mm")
table.add_row("MASSA",f"{massa:.2f} ","kg")

console = Console()
console.print(table)

print()
print()
