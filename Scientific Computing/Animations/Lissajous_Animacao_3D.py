import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math as mt

def retasR3(x,y,z,D): 
   T = np.linspace(-D,D,4000)
   X = T * x
   Y = T * y
   Z = T * z   
   plt.plot(X,Y,Z,color = 'black',linewidth = 0.5)
   

  
def atualizar_Lissajous(frame):
    for plots in [Lissajouses,Pontos]:
        if len(plots)>0:
            plots.pop().remove()
    Lissajous, = plt.plot(X_lissajous[:frame+1], Y_lissajous[:frame+1],Z_lissajous[:frame+1],color = 'firebrick')
    Ponto, = plt.plot(X_lissajous[frame],Y_lissajous[frame],Z_lissajous[frame],'ko',markersize = 4,color='grey')
    Lissajouses.append(Lissajous)
    Pontos.append(Ponto)


if __name__ == '__main__':
    while True:
        Lissajouses = [] #listas que irão armazenar as animações
        Pontos = []
        try:
            #coeficientes da curva de Lissajous
            A = float(input("Insira o Coeficiente A da curva: "))
            a = float(input('Insira o Coeficiente a da curva: '))
            B = float(input("Insira o Coeficiente B da curva: "))
            b = float(input('Insira o Coeficiente b da curva: '))
            phi = np.pi * 1/(float(input('Insira coeficiente de pi do parâmetro phi(pi/input): ')))
            #coeficientes do plano
            ap = float(input('Insira o coeficiente A do plano: '))
            bp = float(input('Insira o coeficiente B do plano: '))
            cp = float(input('Insira o coeficiente C do plano: ')) 
            dp = float(input('Insira o coeficiente D do plano: '))
        except ValueError:
           print('Coeficientes devem ser inseridos como Float, tente novamente')
           break
        D = (A+B)*2
        #prepara o plano para a animação
        fig = plt.figure()
        ax = fig.add_subplot(111,projection = '3d')
        plt.style.use('dark_background')
        ax.grid()
        ax.set_xlabel('Eixo X')
        ax.set_xlim(-D,D)
        ax.set_ylabel('Eixo Y')
        ax.set_ylim(-D,D)
        ax.set_zlabel('Eixo Z')
        ax.set_zlim(-D,D)
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
        Z_plano = (-ap * X_plano -bp * Y_plano + dp)/cp
        ax.plot_surface(X_plano,Y_plano,Z_plano,color = 'black',alpha = .25)
        #rotaciona a camêra 
        try:
            elevacao_radianos  = mt.acos( (ap**2 + bp**2) / mt.sqrt( (ap**2 + bp**2 + cp**2) * (ap**2 + bp**2) ) )
            azimuth_radianos = mt.acos(ap / mt.sqrt(ap**2 + bp**2)) 
        except ZeroDivisionError:
            elevacao_radianos,azimuth_radianos = 1.5707963267948966, 1.5707963267948966
        elevacao = (180/np.pi) * elevacao_radianos
        azimuth =  (180/np.pi) * azimuth_radianos
        ax.view_init(elev=elevacao, azim=azimuth, roll=0)
        #equacoes parametricas da Lissajous
        T = np.linspace(0,70*np.pi,5000)
        X_lissajous = A * np.sin(a * T + phi)
        Y_lissajous = B * np.sin(b * T)
        Z_lissajous = (-ap * X_lissajous -bp * Y_lissajous + dp)/cp
        ani = animation.FuncAnimation(fig, atualizar_Lissajous, frames=5000, interval=60)
        plt.show()
        break
        