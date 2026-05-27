import sys
import numpy as np
import plotext as plt
import argparse
import math as math
from scipy.fft import fft, fftfreq

#arg 0 - nome arquivo
#-x
#-y 
#-d delimiter


parser = argparse.ArgumentParser(description="=== FFT ===")

parser.add_argument("-n", help="Nome do arquivo")
parser.add_argument("-x", default = 0, help="Coluna X")
parser.add_argument("-y", default = 1, help="Coluna Y")
parser.add_argument("-d", default = ';', help="Limitador no csv")

args = parser.parse_args()

nome_arquivo = args.n
col_x = int(args.x)
col_y = int(args.y)
d = args.d

data = np.loadtxt(nome_arquivo, skiprows = 2, delimiter = d)

x = data[:,col_x]
y = data[:,col_y]

time_steps = np.diff(x)
    
# Calculate key statistics
mean_step = np.mean(time_steps)
std_step = np.std(time_steps)
max_step = np.max(time_steps)
min_step = np.min(time_steps)

N = len(x) - 1
T = time_steps

# print("--- Time Array Spacing Analysis ---")
# print(f"Mean Time Step (dt): {mean_step:.6f} s (Equivalent to {1/mean_step:.2f} Hz)")
# print(f"Min Time Step:       {min_step:.6f} s")
# print(f"Max Time Step:       {max_step:.6f} s")
# print(f"Standard Deviation:  {std_step:.6e} s")

yf = fft(y)
xf = fftfreq(N, T)[:N//2]
x_axis =  2.0/N * np.abs(yf[0:N//2])
 
plt.theme('clear')
plt.plot_size(100,30)
plt.plot(xf,x_axis)
plt.show()

f_max = max(yf)
print(f"Frequencia Máxima: {f_max}")
