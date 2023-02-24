# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 18:01:45 2023

@author: E805511
"""

import pymongo

# Criar uma conexão com o servidor MongoDB local
CONNECT_MONGO_TREINAMENTO = "mongodb://treinamento:treinamento@nwautomhml:27017/?authMechanism=DEFAULT&authSource=treinamento"
client = pymongo.MongoClient(CONNECT_MONGO_TREINAMENTO)

# Selecionar um banco de dados
db = client["treinamento"]

# Listar as coleções do banco de dados
print(db.list_collection_names())
