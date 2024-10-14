import numpy as np
import matplotlib.pyplot as plt
from math import exp
 
def trapeziodal(f,a,b,n):
    soma = 0
    h = (b-a)/n
    X = []
    Y = []
    for i in range(n):
        xprox = a + i*h
        X.append(xprox)
        Y.append(f(xprox))
        plt.scatter(xprox,f(xprox),s = 10,color = 'red')
        plt.vlines(xprox,0,f(xprox),color = 'red')
        soma = soma + f(xprox)
    resultado = h*(f(a)/2 + f(b)/2 + soma)
    segmento(X, Y)
    return resultado

def segmento(pontosX,pontosY):
    if pontosX == pontosY:
     n = len(pontosX)
     k=0
     while k <= n:
         plt.plot(pontosX[k], pontosY[k],color = 'red',)
         k = k + 1
        

v = lambda t: 3*(t**2)*exp(t**3)
V = lambda t:exp(t**3)
n = 15

numerico = trapeziodal(v, 0, 1, n)
exata = V(1.) - V(0.)
erro = abs(exata - numerico)

print(erro)

a = 0.0
b = 1.0

nplot = 50
 
t = np.linspace(a,b,nplot)
v = 3.0*(t**2)*np.exp(t**3)

plt.plot(t,v)
plt.xlim(0.0,1.0)
plt.xlabel('t')
plt.ylim(0.0,9.0)
plt.ylabel('v')
plt.fill_between(t,v, facecolor="b",edgecolor = 'k')
plt.show()

            
    






