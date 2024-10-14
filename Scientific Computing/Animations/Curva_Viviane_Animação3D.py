import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

pi = np.pi

def derivada_vetor(X,Y,Z,h):
    t = parametro
    dx = (1/h) * ( X(t + h) - X(t) )
    dy = (1/h) * ( Y(t + h) - Y(t) )
    dz = (1/h) * ( Z(t + h) - Z(t) )
    return [dx,dy,dz]
 

def derivada_tangente(X,Y,Z,h):
    t = parametro
    d2x = ( 1/h**2 ) * (X( t - h ) - 2 * X(t) + X( t + h ))
    d2y = ( 1/h**2 ) * (Y( t - h ) - 2 * Y(t) + Y( t + h ))
    d2z = ( 1/h**2 ) * (Z( t - h ) - 2 * Z(t) + Z( t + h ))
    return [d2x,d2y,d2z]

 
def retasR3(x,y,z,D): 
   T = np.linspace(-D,D,4000)
   X = T * x
   Y = T * y
   Z = T * z   
   plt.plot(X,Y,Z,color = 'black',linewidth = 0.5)


def atualizar_viviane(frame):
    for plots in [vivianes,pontos,tangentes,normais,binormais]:
        if len(plots)>0:
            plots.pop().remove()
    viviane, = plt.plot(X[:frame+1], Y[:frame+1],Z[:frame+1],color = '#4C191B',linewidth = 1.5)
    tangente = ax.quiver(X[frame],Y[frame],Z[frame],Tx[frame],Ty[frame],Tz[frame],pivot = 'tail',color = 'midnightblue')
    normal = ax.quiver(X[frame],Y[frame],Z[frame],Nx[frame],Ny[frame],Nz[frame],pivot = 'tail',color = 'firebrick')
    
    T = [Tx[frame],Ty[frame],Tz[frame]]
    N = [Nx[frame],Ny[frame],Nz[frame]]
    B = np.cross(T,N)
    
    binormal  = ax.quiver(X[frame],Y[frame],Z[frame],B[0],B[1],B[2],pivot = 'tail',color = 'green')
    
    ponto, = plt.plot(X[frame],Y[frame],Z[frame],'ko',markersize = 4)
    
    vivianes.append(viviane)
    tangentes.append(tangente)
    normais.append(normal)
    binormais.append(binormal)
    pontos.append(ponto)


if __name__ == '__main__':
    h = 1e-3
    lista_sim = []
    while True:
        vivianes = []  #listas que irão armazenar as animações    
        pontos = []
        tangentes = []
        normais = []
        binormais = []       
        try: #confere se as entradas sâo válidas
         r = float(input('Insira o raio da curva de viviani: '))
        except ValueError:
            print('Valor inválido, entradas devem ser do tipo "Float", tente novamente... ')
            break
        D = 1.2 * r
        #prepara o espaço para a animação
        fig = plt.figure()
        ax = fig.add_subplot(111,projection = '3d')
        ax.grid()
        ax.set_xlabel('Eixo X')
        ax.set_xlim(-D,D)
        ax.set_ylabel('Eixo Y')
        ax.set_ylim(-D,D)
        ax.set_zlabel('Eixo Z')
        ax.set_zlim(-D,D)
        ax.set_title('Curva de Viviani',fontsize = 20,color = '#4C191B')
        #define os "eixos" da figura
        retasR3(1, 0, 0, D)
        retasR3(0, 1, 0, D)
        retasR3(0, 0, 1, D)
        #desenha a esfera ao qual a curva percorre
        u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
        X_Circulo = r * np.cos(u) * np.sin(v)
        Y_Circulo = r * np.sin(u) * np.sin(v)
        Z_Circulo = r * np.cos(v)
        ax.plot_surface(X_Circulo,Y_Circulo,Z_Circulo,color = '#D3D5D4',alpha = 0.045)
        #funcoes parámetricas e parâmetro da curva de viviani
        parametro = np.linspace(0,6 * pi,500)
        Xt = lambda t: r * np.cos(t) * np.cos(t)
        Yt = lambda t: r * np.cos(t) * np.sin(t)
        Zt = lambda t: r * np.sin(t)
        
        dx = derivada_vetor(Xt, Yt, Zt, h)[0] #Derivadas das funções paramétricas do vetor
        dy = derivada_vetor(Xt, Yt, Zt, h)[1]
        dz = derivada_vetor(Xt, Yt, Zt, h)[2] 
        
        norma_T = np.sqrt(dx**2 + dy**2 + dz**2) #Norma do vetor tangente
        
        Tx = dx / norma_T #Derivadas normalizadas das funções paramétricas do vetor
        Ty = dy / norma_T  
        Tz = dz / norma_T 
        
        d2x = derivada_tangente(Xt, Yt, Zt, h)[0] #Segundas derivadas das funções parámetricas
        d2y = derivada_tangente(Xt, Yt, Zt, h)[1]
        d2z = derivada_tangente(Xt, Yt, Zt, h)[2]
        #Calcula o vetor normal, N(t), através da fórmula:{ r´(t) X ( r´´(t) X r´(t) )  / ||r´(t)|| * ||r´´(t) X r´(t)|| } 
        
        A = ( d2y * dz ) - ( dy * d2z ) #Define as componentes do vetor: r´´(t) X r´(t) = (A,B,C)
        B = ( dx * d2z ) - ( d2x * dz )
        C = ( d2x * dy ) - ( dx * d2y )
        
        Xn = ( dy * C ) - ( dz * B ) #Calcula o produto vetorial: r´(t) X (A,B,C), onde (A,B,C) = r´´(t) X r´(t)
        Yn = ( A * dz ) - ( dx * C )
        Zn = ( dx * B ) - ( A * dy )
         
        norma_vetorial = np.sqrt(A**2 + B**2 + C**2) #Norma do produto vetorial entre a derivada e a segunda derivada( ||r´´(t) X r´(t)|| )
       
        norma_total = norma_T * norma_vetorial  #Norma "Total" do vetor, para normalizar as equações Xn,Yn,Zn acima(||r´(t)|| * ||r´(t) X r´´(t)||)
    
        Nx = Xn / norma_total #Equações parámetricas finais, do vetor N(t) = T´(t) / ||T´(t)||
        Ny = Yn / norma_total
        Nz = Zn / norma_total
        
        X = Xt(parametro) #Np.array com os pontos da Função Paramétrica
        Y = Yt(parametro)
        Z = Zt(parametro)
        ani = animation.FuncAnimation(fig, atualizar_viviane, frames=20000, interval=5*(D/2))
        plt.show()
        break