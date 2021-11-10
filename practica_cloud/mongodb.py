# -*- coding: utf-8 -*-

from pymongo import MongoClient

# Creamos base de datos en Mongo:
client = MongoClient('db', 27017)
db = client.twitterdb 

# Leemos el archivo .json resultado del análisis:   
result_ = open("output.txt")

for line in result_: 
    key, value  = line.split("\t")  
    item_doc = {
       'prop1': key,
       'prop2': value
    }
    db.twitterdb.insert_one(item_doc)
# si queremos insertar varios diccionarios: insert_many
