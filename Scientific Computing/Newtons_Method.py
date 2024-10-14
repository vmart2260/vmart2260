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
            print('Erro! - derivada zero em x =', x)
            SystemExit()
            
        f_x = f(x)
        numero_iteracoes += 1
        
    if abs(f_x) > eps:
        numero_iteracoes = -1
    return x, numero_iteracoes

from random import randint

if __name__ == '__main__':
    def F(t): #função a ser chamada
        return t**2 - 8*t + 15
    
    def dfdt(t): #derivada da função anterior
        return 2*t - 8
    
    R = randint(-100,100)
    Eps = 1.0e-6
    
    solucao, n_iteracoes = Newton(F, dfdt, x=R, eps=Eps)
    
    if n_iteracoes > 0: #confere se uma solução foi achada
        print('Número de vezes em que uma função foi chamada: {:d}'.format(1+2*n_iteracoes))
        print('Uma raíz é: {:f}'.format(solucao))
    else:
        print('Solução não foi achada')
