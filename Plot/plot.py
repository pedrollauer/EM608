import sys
import numpy as np
import plotext as plt
import argparse

#arg 0 - nome arquivo
#-x
#-y 
#-d delimiter


parser = argparse.ArgumentParser(description="=== Plotar dados da linha de comando ===")

parser.add_argument("-n", help="Nome do arquivo")
parser.add_argument("-x", default = 0, help="Coluna X")
parser.add_argument("-y", default = 1, help="Coluna Y")
parser.add_argument("-d", default = ';', help="Limitador no csv")
parser.add_argument("-l", default = None , help="Limite X")

args = parser.parse_args()

nome_arquivo = args.n
col_x = int(args.x)
col_y = int(args.y)
d = args.d
lim = args.l

data = np.loadtxt(nome_arquivo, skiprows = 2, delimiter = d)

x = data[:,col_x]
y = data[:,col_y]

plt.theme('clear')
plt.plot_size(100,30)

if lim != None:
    plt.xlim(float(lim))
plt.plot(y,x)
plt.show()
