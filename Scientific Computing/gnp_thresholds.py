import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from numpy import log, exp, sin, cos, sqrt

fig, ax = plt.subplots()
ax.grid(linewidth=0.20)
#ax.axhline(0,linewidth = 1.5,color="white")
#ax.axvline(0,linewidth = 1.5,color="white")

def Gnp(n,p): return nx.gnp_random_graph(n,p)

def Gnm(n,m): return nx.gnm_random_graph(n,m)

""" Iremos mostrar, numericamente,
    que a função M(N) = nlogn/2 é um sharp threshold
    para a prpriedade de haver pelo menos um vértice isolado"""
numero_simulacoes = 1000
probabilidades = []
"""
for k in range(3,100):
    graus_zero = []
    for sims in range(numero_simulacoes):
        N = k
        #eps = 1e-1
        M = lambda n: 0.5 * n * (log(n) + log(n)/2)
        
        g1 = Gnm(N,M(N))
        graus = [pares[1] for pares in g1.degree]
        grau_minimo = min(graus)
        if grau_minimo == 0:
            graus_zero.append(grau_minimo)
        else:
            pass
    prob_estim = len(graus_zero)/numero_simulacoes
    probabilidades.append(prob_estim)
    
    
nx.draw(g1)
print(prob_estim)
"""


""" Iremos mostrar, numericamente, que p = n^-2 é threshold
para a propriedade do grafo não ser vazio   """

N = 20
n_sims = 100
thresh = lambda n: n**(-2)
thresh = thresh(N)
probs = np.arange(0,1,0.01)
frequencias = []

for p in probs:
    quantidades = 0
    for sims in range(n_sims):
        grafo = Gnp(N,p)
        if grafo.edges:
            quantidades += 1
        if not grafo.edges:
            pass
    frequencia = quantidades/n_sims
    frequencias.append(frequencia)

delta = 0.0031    
ax.plot(probs,frequencias,"lightblue")
ax.axvline(thresh,color="darkgrey")
ax.set_xlabel("p")
ax.set_ylabel("Probabilidade")
ax.set_xlim(0 - 0.15 * delta,thresh + 20 * delta)
ax.set_ylim(0 - 2 * delta,1 + 5 * delta)
ax.set_title("Threshold para Grafo não Vazio")

    
    
    
    
    
    
    
    
    