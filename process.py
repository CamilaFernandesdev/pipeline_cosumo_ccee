# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:57:34 2023

@author: E805511
"""

import pandas as pd
from pathlib import Path
import json

_filepath = Path("C:/Users/E805511/Downloads/Consumo_horario_2022_12/Consumo_horario_2022_12.csv")

# Verificar pq não roda CSV
# df = pd.read_fwf(_filepath)

COLUMNS_DROPED = ['HH',
                        'Cód. Perfil Distribuidora',
                        'Sigla Perfil Distribuidora', 
                        'CNAE']


COLUMNS_DROPED_SHAREPOINT = ['Cód. Perfil', 
                             'Sigla',
                             'Nome Empresarial',
                             'CNPJ da Carga']

CARGA_CODE = ['Cód. Carga']

COLUMNS_NUMERIC_DATA = ['Consumo no Ambiente Livre da parcela de carga - MWh (RC_AL c,j)', 
                        'Consumo de energia ajustado da parcela cativa da carga parcialmente livre - MWh (RC_CAT c,j)', 
                        'Consumo de energia ajustado de uma parcela de carga - MWh (RC c,j)',  
                        'Capacidade da Carga (MW)', 
                        'Consumo de energia no ponto de conexão da parcela de carga - MWh (MED_C c,j)']


RENAMED_COLUMNS = []


# oRGANIZAR
"""
Fazer várias funções
e juntá-las quando estiver processando os dados
"""




process_data = list()
for i, chunk in enumerate(pd.read_csv(_filepath,
                                      sep = ';',
                                      chunksize=10**5,
                                      low_memory=False
                                      )):
    
    chunk = chunk.drop(COLUMNS_DROPED)
    
    
    process_data.append(chunk)
    # 90 travamento total
    if i == 9:
        break    



# Update Mongo
"""
1 - Fazer a média dos dados numéricos
2 - Fazer um drop_duplicate
3 - Concatenar essas informações
4 - Adicionar no Mongo
5 - Segundo dataframe para o sharepoint
"""











lista_empresas = list()
def tratando_dados_empresas(process_data):
    for i, df in enumerate(process_data):
        df = process_data[i]
        # Separando os dados empresariais e tratando-o em outro dataframe
        columns_dados_empresas = ['Cód. Perfil', 'Sigla', 'Classe do perfil do agente','Nome Empresarial', 'Cód. Carga', 'Carga', 'CNPJ da Carga', 'Cidade','Estado', 'Submercado','Ramo de Atividade']
        df_dados_empresariais = df[columns_dados_empresas]
        
        df_dados_empresariais.set_index('Cód. Carga', inplace=True)
        df_dados_empresariais = df_dados_empresariais.drop_duplicates()
        
        
        lista_empresas.append(df_dados_empresariais)

# lista_dados = list()
# def tratando_process_data(process_data):
#     for i, df in enumerate(process_data):
#         df = process_data[i]
#         # Separando os dados empresariais e tratando-o em outro dataframe
#         columns_droped = ['Cód. Perfil',
#                           'Nome Empresarial',
#                           'Sigla','Nome Empresarial',
#                           'Carga', 'CNPJ da Carga', 'CNAE']
#         df = df.drop(columns=columns_droped)
#         df.set_index(['Data'], inplace=True)
#         lista_dados.append(df)



# tratando_dados_empresas(process_data)
# tratando_process_data(process_data)
# #%% Two step

# =============================================================================
# Teste com um dataframe sample
def processar_dados_numericos():
    pass

df = process_data[0]
df = df[COLUMNS_NUMERIC_DATA]
df.set_index(['Cód. Carga'], inplace=True)
df = df.replace(',', '.', regex=True)
df = df.astype(float)
df = df.groupby('Cód. Carga').mean()
# =============================================================================
# b = pd.PeriodIndex(df.index.get_level_values('Data'), freq="T")

# Dados sem as médias
teste = lista_dados[0]
teste = teste.drop(columns=['HH', 'Consumo no Ambiente Livre da parcela de carga - MWh (RC_AL c,j)',
'Consumo de energia ajustado da parcela cativa da carga parcialmente livre - MWh (RC_CAT c,j)',
'Consumo de energia ajustado de uma parcela de carga - MWh (RC c,j)',
 'Consumo de energia no ponto de conexão da parcela de carga - MWh (MED_C c,j)']).drop_duplicates()

# teste = teste.groupby('Cód. Carga').agg('mean')


