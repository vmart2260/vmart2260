import numpy as np 
import pandas as pd 
from scipy import optimize as opt
from yfinance import download

"O Código a seguir tem como objetivo calcular os portfolios ótimos 'em volta' do portfolio com sharpe ótimo."
"Assim, espera-se conseguir a alocação ótima (com 6 ações no mínimo) que melhor aproxima o portfolio ótimo de sharpe"
"Para tal fim, calcula-se os portfolios ótimos em um intervalo [-N*eps , +N*eps] em volta do portfolio com sharpe ótimo e"
"filtra-se os portfolios que possuem menos de 6 ações. Após isso, acha-se o portfolio com maior retorno e utilizamos ele como alocação ótima"

ativos_preco = download(
["MGLU3.SA",
"AZUL4.SA",
"BHIA3.SA",
"ENEV3.SA",
"BOVA11.SA",
"BRL=X",
"EMBR3.SA",
"PRIO3.SA",
"FHER3.SA",
"LOGN3.SA"],start="2022-01-03")["Adj Close"]
ativos_preco.interpolate(method='linear',inplace=True)
dados = ativos_preco.pct_change().dropna()  
retornos_medios = dados.mean()
covariance_matrix = dados.cov()

transformar_pctg = lambda n: np.round(n * 100,2) # transforma um número (n) em porcentagem (é utilizado na linha 53 para conferir se os pesos são iguais a 0)

def varianca(pesos): # calcula a varianca diára de um portfolio
    return np.dot(pesos.T,(np.dot(covariance_matrix,pesos)))

def sharpe_min(pesos): # calcula o "sharpe diário" de um portfólio e multiplica por -1. fazemos isso para utilizar essa mesma função no algoritmo de minimização
    pesos = np.array(pesos) # caso não seja um array
    retorno_port = np.sum((dados.mean() * pesos)) # retorno diário do portfolio
    vol_port = np.sqrt(np.dot(pesos.T, np.dot(covariance_matrix, pesos))) # vol diária do portfolio
    Rf = 0.04467/(252 * 2.5) # taxa livre de risco do T2, diarizada
    
    return (retorno_port - Rf) / vol_port



pesos_iniciais = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]) # define um portfolio inicial arbitrário(nesse caso, com pesos iguais)
limites = tuple((0,(1/6)) for x in range(10)) # define máximos e mínimos para os pesos individuais (não é aceito portfolios com tudo em um ativo, e nem portfolios sem um ativo)
restricao1 = {'type' : 'eq' , 'fun' : lambda pesos: np.sum(pesos) - 1} # soma dos pesos tem que ser igual a 1 (100%)
                                                                                                 
max_sharpe = opt.minimize(sharpe_min,pesos_iniciais,method='SLSQP',bounds=limites,constraints=(restricao1)) # acha o portfolio com o maior índice de sharpe diário
retorno_sharpe = np.sum(dados.mean() * -max_sharpe['x']) # retorno médio diario do portfolio com melhor sharpe, em %
Rp = retorno_sharpe * 1e-2 # retorno médio, em número

                                                                                           

restricao_eps_mais = lambda eps,n: {'type':'eq','fun':lambda pesos: retornos_medios.dot(pesos) - Rp-(n*eps)} # dado um valor de n e eps, define as restrições relacionada aos retornos contidos em [Rp,+N*eps]
restricao_eps_menos = lambda eps,n: {'type':'eq','fun':lambda pesos: retornos_medios.dot(pesos) - Rp+(n*eps)} # dado um valor de n e eps, define as restrições relacionada aos retornos contidos em [-N*eps,Rp]


def portfolios_eps(): # calcula os retornos dos portfólios ótimos em volta do portfólio de sharpe ótimo
    eps = 1* 1e-6 # valores arbitrário
    N = 15
    retornos_eps_mais = [opt.minimize(varianca,pesos_iniciais,method='SLSQP',bounds=limites,constraints=(restricao1,restricao_eps_mais(eps,n)))['x'] for n in np.arange(0,N,100)] # calcula os retornos dos portfólios ótimos em [Rp,+N*eps]
    retornos_eps_menos = [opt.minimize(varianca,pesos_iniciais,method='SLSQP',bounds=limites,constraints=(restricao1,restricao_eps_menos(eps,n)))['x'] for n in np.arange(0,N,100)] # calcula os retornos dos portfólios ótimos em [-N*eps,Rp]
       
    
    return retornos_eps_menos + retornos_eps_mais


def pesos_validos(lista_arrays=portfolios_eps()): # filtra os portfolios com menos de 6 ativos
    pesos = []
    for array in lista_arrays:
       array = transformar_pctg(array) # transforma em porcentagem para fins de comparação
       nao_zeros = [peso for peso in array if peso != 0.0] # constrói lista de não zeros
       if len(nao_zeros) >= 6:
           pesos.append(array)
       else:
           pesos = pesos
           
    return pesos
 
retornos_portfolios_eps = [np.sum(pesos * retornos_medios) for pesos in pesos_validos()] # calcula os retornos dos portfólios filtrados
Rpmax = max(retornos_portfolios_eps) # maior retorno
indice_peso = retornos_portfolios_eps.index(Rpmax) # indice do portfolio com maior retorno, usado para achar a alocação do mesmo em pesos_validos()
peso_final = pesos_validos()[indice_peso] # alocação com maior retorno em um intervalo [-N*eps,+N*eps] de retornos, centrado no Rp


