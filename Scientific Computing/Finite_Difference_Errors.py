import matplotlib.pyplot as plt
import numpy as np

"O código a seguir usa uma função, sua derivada, e os métodos de diferença finita (h = 2pi/2^n) para calcular e desenhar os gráficos das aproximações de cada método"
"junto da derivada analítica (desenho à esquerda). O código também calcula e desenha os erros dos respectivos métodos, junto do erro cometido pela aproximação atual"
"e sua posição no gráfico (desenho à direita)."

fig, ((ax1,ax2), (ax3,ax4), (ax5,ax6)) = plt.subplots(3,2) # define uma grade 3x2 de plots para desenhar os gráficos
pi = np.pi

f = lambda x: np.sin(x) # função que se deseja derivar
cos = lambda x: np.cos(x) # derivada analítica 
f_dif = lambda x,h: (f(x + h) - f(x)) / h # formula da diferença "para frente"
b_dif = lambda x,h: (f(x) - f(x - h)) / h # formula da diferença "para trás"
c_dif = lambda x,h: (f(x + (h/2)) - f(x - (h/2))) / h # formula da diferença "central"


n = 7 # controla o refinamento da malha
h = (2*pi) / (2**n) # tamanho dos subintervalos da malha
intervalo = np.arange(0,2*pi,h) # malha com subintervalos de tamanho (h) e (2^n) elementos
intervalo_refinado = np.linspace(0,2*pi,1000) # malha com mil pontos para a o calculo e grafico da derivada analítica, para fins de comparação e desenho da derivada analítica

forward_dif = [f_dif(x,h) for x in intervalo]# calcula a diferença "para frente" nos pontos apropriados
backward_dif = [b_dif(x,h) for x in intervalo] # calcula a diferenças "para trás" nos pontos apropriados
central_dif = [c_dif(x,h) for x in intervalo] # calcula a diferença "central" nos pontos apropriados

 # prepara o plano 1x1 para o desenho do gráfico
ax1.set_xlabel('x axis ')  
ax1.axhline(0,color = 'white', linewidth = 0.5)
ax1.set_ylabel('y axis') 
ax1.axvline(0,color = 'white', linewidth = 0.5)
ax1.grid(linewidth = 0.25)
ax1.set_aspect('equal')
ax1.set_title('Foward Diference')

ax1.plot(intervalo,forward_dif,color = "lightblue",label = "foward diference") # desenha a curva calculada pelo o método da diferenca para frente
ax1.plot(intervalo_refinado,cos(intervalo_refinado),color = "darkblue",label = "analytical derivative") # desenha a curva da derivada analítica
ax1.legend(loc="best")

 # prepara o plano 1x2 para o desenho do gráfico
ax3.set_xlabel('x axis')  
ax3.axhline(0,color = 'white', linewidth = 0.5)
ax3.set_ylabel("y axis") 
ax3.axvline(0,color = 'white', linewidth = 0.5)
ax3.grid(linewidth = 0.25)
ax3.set_aspect('equal')
ax3.set_title('Backwards Diference')

ax3.plot(intervalo,backward_dif,color = "lightblue",label = "backwards diference") # desenha a curva calculada pelo o método da diferenca para trás
ax3.plot(intervalo_refinado,cos(intervalo_refinado),color = "darkblue",label = "analytical derivative") # desenha a curva da derivada analítica
ax3.legend(loc="best")

 # prepara o plano 1x3 para o desenho do gráfico
ax5.set_xlabel('x axis')  
ax5.axhline(0,color = 'white', linewidth = 0.5)
ax5.set_ylabel("y axis") 
ax5.axvline(0,color = 'white', linewidth = 0.5)
ax5.grid(linewidth = 0.25)
ax5.set_aspect('equal')
ax5.set_title('Central Diference')

ax5.plot(intervalo,central_dif,color = "lightblue",label = "central diference") # desenha a curva calculada pelo o método da diferenca central
ax5.plot(intervalo_refinado,cos(intervalo_refinado),color = "darkblue",label = "analytical derivative") # desenha a curva da derivada analítica
ax5.legend(loc="best")


H = lambda n: (2*pi) / (2**n) # define h como função de n
f_error = lambda n: abs(cos(pi) - f_dif(pi,H(n))) # calcula o erro da diferença "para frente" em função de n
b_error = lambda n: abs(cos(pi) - b_dif(pi,H(n))) # calcula o erro da diferença "para trás" em função de n
c_error = lambda n: abs(cos(pi) - c_dif(pi,H(n))) # calcula o erro da diferença "central" em função de n

intervalo_dosN = range(3,16) # intervalo sobre o qual sera calculado o erro
intervalo_dosN = np.array([intervalo_dosN[len(intervalo_dosN) - i] # inverte a ordem do intervalo para visualização contra o eixo (Log2(h))
                         for i in range(1, len(intervalo_dosN)+1)]) 

forward_errors = [f_error(n) for n in intervalo_dosN] # calcula os erros da diferença "para frente"
backwards_errors = [b_error(n) for n in intervalo_dosN] # calcula os erros da diferença "para frente"
central_errors = [c_error(n) for n in intervalo_dosN] # calcula os erros da diferença "para frente"

eixo_log = np.log2(H(intervalo_dosN)) # malha com os valores de log2(h) que serão utilizados no desenho do gráfico
N = np.log2(2*pi) - n # variável criada para facilitar compreensão do código, utilizada no desenho do ponto de erro do n atual(linhas 90,103,116) 


# prepara o plano 2x1 para o desenho do gráfico
ax2.set_xlabel('log2(h)') 
ax2.axhline(0,color = 'white', linewidth = 0.5)
ax2.set_ylabel("error")
ax2.set_yscale("log")  
ax2.axvline(0,color = 'white', linewidth = 0.5)
ax2.grid(linewidth = 0.25)
ax2.set_title('Foward Diference Error on x=%s' %chr(960))

ax2.plot(eixo_log,forward_errors,color = "firebrick") # desenha o gráfico do erro da diferença para frente contra o log2(h)
ax2.plot(N,f_error(n),color = "lightblue",marker = "o",markersize = 5,label = "erro de n=%d igual a %f" % (n,f_error(n))) # marca no grafico onde esta o erro do calculo do n atual e informa seu valor numérico
ax2.legend(loc="best")

# prepara o plano 2x2 para o desenho do gráfico
ax4.set_xlabel('log2(h)')  
ax4.axhline(0,color = 'white', linewidth = 0.5)
ax4.set_ylabel("error") 
ax4.set_yscale("log")
ax4.axvline(0,color = 'white', linewidth = 0.5)
ax4.grid(linewidth = 0.25)
ax4.set_title('Backwards Diference Error on x=%s' %chr(960))

ax4.plot(eixo_log,backwards_errors,color = "firebrick") # desenha o gráfico do erro da diferença para trás contra o log2(h)
ax4.plot(N,b_error(n),color = "lightblue",marker = "o",markersize = 5, label = "erro de n=%d igual a %f" % (n,b_error(n)) ) # marca no grafico onde esta o erro do calculo do n atual e informa seu valor numérico
ax4.legend(loc="best")

# prepara o plano 2x3 para o desenho do gráfico
ax6.set_xlabel('log2(h)')
ax6.axhline(0,color = 'white', linewidth = 0.5)
ax6.set_ylabel("error")
ax6.set_yscale("log") 
ax6.axvline(0,color = 'white', linewidth = 0.5)
ax6.grid(linewidth = 0.25)
ax6.set_title('Central Diference Error on x=%s' %chr(960))

ax6.plot(eixo_log,central_errors,color = "firebrick") # desenha o gráfico do erro da diferença central contra o log2(h)
ax6.plot(N,c_error(n),color = "lightblue",marker = "o",markersize = 5,label = "erro de n=%d igual a %f" % (n,c_error(n)) ) # marca no grafico onde esta o erro do calculo do n atual e informa seu valor numérico
ax6.legend(loc="best")


fig.suptitle("Diferenças para n=%d e Erros" % n) # titulo de todos os gráficos
plt.tight_layout(pad=0.00001) # ajusta o espaçamento entre gráficos para evitar overlaping dos títulos,subtítulos,labels,etc
plt.show() 

