def Newton(f,dfdx,x,eps):
    '''Recebe uma função [f], sua derivada [dfdx], um valor inicial para x [x] e um valor para o erro entre a função e a raiz [eps];
    retorna uma raiz X  e o número de vezes em que uma função foi chamamada
    '''
    numero_iteracoes = 0
    n = 100 #número máximo de iterações permitidas
    f_x = f(x)
    while abs(f_x) > eps and numero_iteracoes < n: # interrompe o programa caso a função esteja no intervalo ou n tenha sido atingido 
    
        try: #interrompe o programa caso a derivada seja = 0
            x = x - f_x/dfdx(x)
        except ZeroDivisionError:
            SystemExit()
            
        f_x = f(x)
        numero_iteracoes += 1
        
    if abs(f_x) > eps:
        numero_iteracoes = -1
    return x, numero_iteracoes


def Desenho():
 from matplotlib import pyplot as plt
 import numpy as np    

 X = np.linspace(-50,50,20000)
 y = F(X)
 raizes = lista_raizes
 Fraizes = np.zeros_like(lista_raizes)
 
 plt.style.use('dark_background')
 
 plt.grid(linewidth=0.15)
 plt.axhline(color = 'white')
 plt.axvline(color = 'white')
 
 plt.axis([-10,10,-20,20])
 plt.hlines(0,-5,10,color = 'white')
 plt.vlines(0,-10,15, color = 'white')

 plt.xlabel('x')
 plt.ylabel('f(x)')

 plt.plot(X,y, color = 'red')
 plt.scatter(raizes,Fraizes, color='blue')
 plt.show()   


if __name__ == '__main__':
    from random import randint
    def F(t): #função a ser chamada
        return t**2 + 3*t - 18
    
    def dfdt(t): #derivada da função anterior
        return 2*t + 3
    
    #R = float(randint(-10,10))
    Eps = 1.0e-6
    K = 10000

  #  solucao, n_iteracoes = Newton(F, dfdt, x=R, eps=Eps)
    lista_raizes = []
    i = 0
    while i < K: 
     R = float(randint(-100,100))
     solucao, n_iteracoes = Newton(F, dfdt, R, eps=Eps)
     solucao_arredondada = round(solucao)
     if n_iteracoes > 0 and solucao_arredondada not in lista_raizes: #confere se uma solução foi achada
         print('Número de vezes em que uma função foi chamada: {:d}'.format(1+2*n_iteracoes))
         print('Uma raíz é: {:f}'.format(solucao))
         lista_raizes.append(solucao_arredondada)
         i += 1
     #if n_iteracoes > 0 and solucao_arredondada in lista_raizes:
        # a = a - 1
         #K = K + 1
     else:
         i += 1
    Kstr = str(K)
    Lstr = str(lista_raizes)
    print('As raízes da função, após {K} aplicações do Método de Newton foi {L}'.format(K = Kstr, L = Lstr))
    Desenho()


    
    
    
    
    
    
    
    
    
    
    