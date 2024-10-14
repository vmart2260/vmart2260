import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from numpy import exp, arcsin

plt.style.use("dark_background")
fig, ax = plt.subplots()
ax.set_xlabel("t")
ax.axhline(0,color="white",linewidth=1)
ax.set_ylabel("x(t)")
ax.axvline(0,color="white",linewidth=1)
ax.set_title("Método de Euler",loc="Left")
ax.grid(linewidth=0.25)

# Variáveis globais
global glob_h, glob_t, glob_y, glob_odefun


def feuler(odefun, tspan, y0, Nh):
    """ Recebe uma função (odefun), um vetor de condições iniciais (y0), 
    uma lista com dois valores (min,max) para a váriavel independente t (tspan) e um número de passos (Nh) e retorna um vetor coluna com os dados de tspan
    e suas respectivas aproximações pelo método de euler"""
    h = (tspan[1] - tspan[0]) / Nh # calcula o tamanho do passo
    y = np.array(y0).reshape(-1, 1)  # cria um vetor coluna com as condições inciais 
    w = y
    u = y.T # transpõe o vetor coluna de condições iniciais
    tt = np.linspace(tspan[0], tspan[1], Nh + 1) # cria

    for t in tt[:-1]:
        w = w + h * odefun(t, w)
        u = np.vstack((u, w.T))

    t = tt.reshape(-1, 1)
    return t, u

# Função auxiliar para o método de Euler Implícito (Backward Euler)
def beulerfun(w):
    """
    Função que define a equação a ser resolvida pelo método de Euler Implícito.
    
    Parâmetros:
    w - Aproximação atual da solução
    
    Retorna:
    O resultado da equação para a aproximação atual.
    """
    global glob_h, glob_t, glob_y, glob_odefun
    return np.array(w - glob_y - glob_h * glob_odefun(glob_t, w)).flatten()

# Função principal para resolver ODE usando o método de Euler Implícito
def beuler(odefun, tspan, y0, Nh, *args):
    """
    Resolve equações diferenciais usando o método de Euler Implícito (Backward Euler).
    
    Parâmetros:
    odefun - Função que define a equação diferencial
    tspan - Intervalo de tempo [t0, tf]
    y0 - Condição inicial
    Nh - Número de intervalos
    *args - Parâmetros adicionais para a função odefun
    
    Retorna:
    t - Vetor coluna com os tempos
    u - Solução da ODE em cada passo de tempo
    """
    global glob_h, glob_t, glob_y, glob_odefun

    # Cria um vetor de tempos igualmente espaçados
    tt = np.linspace(tspan[0], tspan[1], Nh + 1)
    # Converte a condição inicial em um vetor coluna
    y = np.array(y0).reshape(-1, 1)
    # Inicia a matriz de soluções com a condição inicial
    u = y.T
    
    # Calcula o tamanho do passo
    glob_h = (tspan[1] - tspan[0]) / Nh
    glob_y = y
    glob_odefun = lambda t, y: odefun(t, y, *args)
    glob_t = tt[1]
    
    # Loop através de cada passo de tempo
    for glob_t in tt[1:]:
        # Resolve a equação não linear usando fsolve
        w = fsolve(beulerfun, glob_y.flatten(), xtol=1e-12, maxfev=10000)
        w = w.reshape(-1,1)
        # Adiciona a nova solução à matriz de soluções
        u = np.vstack((u, w.T))
        # Atualiza glob_y para a próxima iteração
        glob_y = w
    
    # Converte o vetor de tempos em um vetor coluna
    t = tt.reshape(-1, 1)
    return t, u


def odefun(t, y, *args): return np.cos(2 * y)

tspan = [0, 1]
y0 = [0]
Nh = 5
t2, u2 = beuler(odefun, tspan, y0, Nh)

def solution(t): return 0.5 *  arcsin((exp(4 * t) - 1) / (exp(4 * t) + 1))

t_foward,u_foward = feuler(odefun,tspan,y0,Nh)
t_backward, u_backward = beuler(odefun, tspan, y0, Nh)
T = np.linspace(0,1,100)


plt.plot(t_foward,u_foward,color = "green", label = "Foward Euler")
plt.plot(T,solution(T), color = "darkblue",label= "Analytic Solution")
plt.plot(t_backward,u_backward,color = "red",label = "Backward Euler")


#####################################################################################
##################################################################################
#####################################################################################

# Vetores para armazenar os erros
fe = []
be = []


# Loop para calcular e comparar os erros dos métodos de Euler Explícito e Implícito
for k in range(10):
    # Método de Euler Explícito
    t, ufe = feuler(odefun, tspan, y0, Nh)
    fe.append(abs(ufe[-1] - solution(t[-1]))[0])
    
    # Método de Euler Implícito
    t, ube = beuler(odefun, tspan, y0, Nh)
    be.append(np.max(abs(ube - solution(t))))
    
    # Dobrar o número de intervalos
    Nh = 2 * Nh

# Exibir os erros
print("Erros do método de Euler Explícito:", fe)
print("Erros do método de Euler Implícito:", be)

ax.legend()