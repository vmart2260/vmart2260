import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import sqrt, acos

def retasR3(x,y,z,D): 
   T = np.linspace(-D,D,4000)
   X = T * x
   Y = T * y
   Z = T * z   
   plt.plot(X,Y,Z,color = 'black',linewidth = 0.5)


    
def atualizar_epicicloide(frame):
    for plots in [epicicloides,Circulos_Fora,Pontos,Raiozinhos]:
        if len(plots)>0:
            plots.pop().remove()
    epicicloide, = plt.plot(X_epicicloide[:frame+1], Y_epicicloide[:frame+1],Z_epicicloide[:frame+1],color = 'firebrick')
    Circulo_Fora, = plt.plot(X_centro[frame] + X_CirculoFora, Y_centro[frame] + Y_CirculoFora,Z_centro[frame] + Z_CirculoFora, color = 'midnightblue')
    Ponto, = plt.plot(X_epicicloide[frame],Y_epicicloide[frame],Z_epicicloide[frame],'ko',markersize = 4,color='grey')
    epicicloides.append(epicicloide)
    Circulos_Fora.append(Circulo_Fora)
    Pontos.append(Ponto)


if __name__ == '__main__':
    lista_sim = []
    while True:
        epicicloides = [] #listas que irão armazenar as animações
        Circulos_Fora = []
        Pontos = []
        Raiozinhos = []
        try: #confere se as entradas sâo válidas
         R = float(input("Insira o Raio do Círculo Interior: "))
         r = float(input('Insira o Raio do curculo Exterior: '))
         a = float(input('Insira o coeficiente A de x: '))
         b = float(input('Insira o coeficiente B de y: '))
         c = float(input('Insira o coeficiente C de z: '))
         d = float(input('Insira o coeficiente D: '))
        except ValueError:
            print('Valor inválido, entradas devem ser do tipo "Float", tente novamente... ')
            break
        D = (R+r)*2
        #prepara o plano para a animação
        fig = plt.figure()
        ax = fig.add_subplot(111,projection = '3d')
        plt.style.use('dark_background')
        ax.grid(visible=False,which='minor')
        ax.set_xlabel('x')
        ax.set_xlim(-D,D)
        ax.set_ylabel('y')
        ax.set_ylim(-D,D)
        ax.set_zlabel('z')
        ax.set_zlim(-D,D)
        T = np.linspace(0,70*np.pi,2000)
        A = np.linspace(0,2*np.pi,100)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
       
        #define os "eixos" da figura
        retasR3(1, 0, 0, D)
        retasR3(0, 1, 0, D)
        retasR3(0, 0, 1, D)
        #desenha o plano da figura
        x_plano, y_plano = np.linspace(-D,D,200) , np.linspace(-D,D,200)
        X_plano,Y_plano = np.meshgrid(x_plano,y_plano)
        Z_plano = (-a * X_plano -b * Y_plano + d)/c
        ax.plot_surface(X_plano,Y_plano,Z_plano,color = 'black',alpha = .25)
        #rotaciona a camêra 
        try:
            elevacao_radianos  = acos( (a**2 + b**2) / sqrt( (a**2 + b**2 + c**2) * (a**2 + b**2) ) )
            azimuth_radianos = acos(a / sqrt(a**2 + b**2)) 
        except ZeroDivisionError:
            elevacao_radianos,azimuth_radianos = 1.5707963267948966, 1.5707963267948966
        elevacao = (180/np.pi) * elevacao_radianos
        azimuth =  (180/np.pi) * azimuth_radianos
        ax.view_init(elev=elevacao, azim=azimuth, roll=0)
        #equacoes parametricas do epicicloide
        X_epicicloide = (R+r) * np.cos(T) - r * np.cos((R+r)*T/r)
        Y_epicicloide = (R+r) * np.sin(T) - r * np.sin((R+r)*T/r)
        Z_epicicloide = (-a * X_epicicloide -b * Y_epicicloide + d)/c
        #equacoes parametricas do circulo de fora, sem incluir seu centro
        X_CirculoFora = r * np.cos(A)
        Y_CirculoFora = r * np.sin(A)
        Z_CirculoFora = (-a * X_CirculoFora -b * Y_CirculoFora + d)/c
        # equacoes parametricas do circulo de dentro
        X_CirculoDentro = R * np.cos(A)
        Y_CirculoDentro = R * np.sin(A) 
        Z_CirculoDentro  = (-a * X_CirculoDentro -b * Y_CirculoDentro + d)/c
        #equacoes parametrica do centro do circulo de fora
        X_centro = (R+r) * np.cos(T)
        Y_centro = (R+r) * np.sin(T)
        Z_centro = (-a * X_centro -b * Y_centro + d)/c
        plt.plot(X_CirculoDentro,Y_CirculoDentro,Z_CirculoDentro,color = 'mediumslateblue')
        ani = animation.FuncAnimation(fig, atualizar_epicicloide, frames=20000, interval=25*(D/2))
        plt.show()
        break
    
        
