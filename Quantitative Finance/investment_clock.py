import numpy as np
import vectorbt as vbt
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime
from datetime import timedelta
from yfinance import download

url_pib = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.22099/dados?formato=json'
url_ipca = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json'

pib = pd.read_json(url_pib)
ipca = pd.read_json(url_ipca)

# transforma a coluna data de formato 'str' para 'datetime'
ipca.data = pd.to_datetime(ipca.data)
pib.data = pd.to_datetime(pib.data)

#transforma o data frame em série temporal, com 'data' sendo seu índice
ipca.set_index(ipca.data,inplace=True)
pib.set_index(pib.data,inplace=True)

# remove a coluna data
pib.drop(
    columns='data',
    inplace=True,
    )

ipca.drop(
    columns='data',
    inplace=True,
    )


# iguala as datas iniciais do data frame
primeira_data = max(ipca.index[0],pib.index[0])
ipca.drop(
    labels=[i for i in ipca.index if i<primeira_data],
    inplace=True
    )

pib.drop(
    labels=[i for i in pib.index if i<primeira_data],
    inplace=True
    )


# Cria uma série temporal com os valores do pib, mensalmente
pib = pd.Series(
    data=[float(pib.loc[data]) if data in pib.index else None for data in ipca.index],
    index=ipca.index
    )

pib = pib.ffill()

# muda o nome das colunas para melhor visualização e entendimento do código
pib.name = 'PIB'
ipca = ipca.rename(columns={'valor':"IPCA"})

# dataframe com dados do IPCA e PIB
df = pd.merge(pib,ipca,left_index=True,right_index=True)

########################################################
#   Cria um dataframe com dados sobre o regime de inflação\crescimento econômico
# (se um esta alto ou baixo) de acordo com valores em 'cortes'

#   Decide a "Fase" em que a Econômia se encontra de acordo com a 
# filosofia de investimentos macro da Meryl Lynch, apelidada de "Investment Clock"
########################################################

def Investment_Clock(dados,cortes={'PIB': 100.0,"IPCA":1.0}):
    dados_ = dados.copy().assign(Crescimento=None,Inflação=None,Fase=None)
    
    # define regimes de crescimento\decaimento econômico
    dados_.loc[dados['PIB'] <= cortes["PIB"],'Crescimento'] = "Baixo"
    dados_.loc[dados['PIB'] > cortes["PIB"],'Crescimento'] = "Alto"
    
    # define regimes de crescimento\decaimento da inflação
    dados_.loc[dados['IPCA'] <= cortes["IPCA"],'Inflação'] = "Baixo"
    dados_.loc[dados['IPCA'] > cortes["IPCA"],'Inflação'] = "Alto"
    
    # define fases do investment clock
    dados_.loc[(dados_.Crescimento=="Baixo") & (dados_.Inflação=="Baixo"),'Fase'] = 'Reflação'
    dados_.loc[(dados_.Crescimento=="Alto") & (dados_.Inflação=="Baixo"),'Fase'] = 'Recuperação'
    dados_.loc[(dados_.Crescimento=="Alto") & (dados_.Inflação=="Alto"),'Fase'] = 'Superaquecimento'
    dados_.loc[(dados_.Crescimento=="Baixo") & (dados_.Inflação=="Alto"),'Fase'] = 'Stagflação'

    return dados_
    
#######################################################

universo_ativos = pd.read_csv(r'C:\Users\Vitor\Desktop\FUNDO_TESTE\1_ativos_teste.csv')
ativos_financeiros = universo_ativos.set_index(universo_ativos['Setor']).loc["Financeiro"]["Ativo"]
ativos_financeiros.reset_index(drop=True,inplace=True)

"""
df_ativos = vbt.YFData.download(
    ["PETR4.SA"],
    interval = "1m",
    start = data_inicial,
    end = data_final,
    missing_index='drop').get("Close")


def Indicador_Ciclo(retornos):
    pass
"""    
    
    
    
    
    
    
    
    
    
    
    
