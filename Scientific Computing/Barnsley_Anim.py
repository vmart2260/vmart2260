import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

plt.style.use('dark_background')
fig = plt.figure()

plt.xlim(-3,3)
plt.ylim(-1,11)

plt.gca().set_xticks([])
plt.gca().set_yticks([])

def funcao1(x,y):
    return (0.0,0.16*y)
def funcao2(x,y):
    return (0.85*x + 0.04*y,-0.04*x + 0.85*y + 1.6)
def funcao3(x,y):
    return(0.2*x - 0.26*y,0.23*x + 0.22*y + 1.6)
def funcao4(x,y):
    return(-0.15*x + 0.28*y, 0.26*x + 0.24*y + 0.44)
funcoes = [funcao1,funcao2,funcao3,funcao4]

def barnsley_gerador(n):
    iteracoes = n-1
    x,y = 0,0
    pontos_x = []
    pontos_y = []
    for n in range(iteracoes):
        funcao_escolhida = np.random.choice(funcoes,p = [0.01,0.85,0.07,0.07])
        x,y = funcao_escolhida(x,y)
        pontos_x.append(x)
        pontos_y.append(y)
    return pontos_x, pontos_y
   


#folhas = np.array([barnsley_gerador(k) for k in np.arange(0,100000,100)])
folhas=[]
contagens = []
quant1 = np.arange(0,500,1)
quant2 = np.arange(500,1000,5)
quant3 = np.arange(1000,2000,10)
quant4 = np.arange(2000,10000,100)

quant1 = np.union1d(quant1,quant2)
quant2 = np.union1d(quant3,quant4)

quantidades = np.union1d(quant1,quant2)

sc = plt.scatter([], [], s=0.2, color='green')
legend_text = plt.text(
    -2.5,
    9,
    '',
    fontsize=12,
    color='grey',
    bbox=dict(facecolor='#3b3b3b',edgecolor='black'),
    )

def anim_func(frame):            
    n = quantidades[frame]
    
    pontos_x, pontos_y = barnsley_gerador(n)
    
    sc.set_offsets(np.c_[pontos_x,pontos_y])
    
    legend_text.set_text(f'n = {n}')

ani = animation.FuncAnimation(fig, anim_func, frames=len(quantidades), interval=30)
plt.show()
        