import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

fig, ax = plt.subplots()

R,r = 3.1415, 1


V = abs(R/r)

K = 50*(1/V)

D = (R+r)*2
ax.set_xlabel('x')
ax.set_xlim(-D,D)
ax.axhline(0,color = 'black', linewidth = 1)
ax.set_ylabel('y') 
ax.set_ylim(-D,D)
ax.axvline(0,color = 'black', linewidth = 1)
ax.grid(linewidth=0.25)
ax.set_aspect('equal')
ax.set_title('Epicicloide')



T = np.linspace(0,70*np.pi,2000)
A = np.linspace(0,2*np.pi,100)


X_epicicloide = (R+r) * np.cos(T) - r * np.cos((R+r)*T/r)
Y_epicicloide = (R+r) * np.sin(T) - r * np.sin((R+r)*T/r)

X_CirculoFora, Y_CirculoFora = r * np.cos(A), r * np.sin(A)
X_CirculoDentro, Y_CirculoDentro = R * np.cos(A), R * np.sin(A)



epicicloides = []
Circulos_Fora = []
Pontos = []
Raiozinhos = []

plt.plot(X_CirculoDentro,Y_CirculoDentro,color = 'mediumslateblue')
    
def atualizar(frame):
    for plots in [epicicloides,Circulos_Fora,Pontos,Raiozinhos]:
        if len(plots)>0:
            plots.pop().remove()
    epicicloide, = plt.plot(X_epicicloide[:frame+1], Y_epicicloide[:frame+1],color = 'firebrick')
    Circulo_Fora, = plt.plot(X_centro[frame] + X_CirculoFora, Y_centro[frame] + Y_CirculoFora, color = 'midnightblue')
    Ponto, = plt.plot(X_epicicloide[frame],Y_epicicloide[frame],'ko',color = 'red',markersize = 7)
    #Raiozinho = plt.plot()
    epicicloides.append(epicicloide)
    Circulos_Fora.append(Circulo_Fora)
    Pontos.append(Ponto)


X_centro = (R+r) * np.cos(T)
Y_centro = (R+r) * np.sin(T)

ani = animation.FuncAnimation(fig, atualizar, frames=2000, interval=75*V)


plt.show()  
    