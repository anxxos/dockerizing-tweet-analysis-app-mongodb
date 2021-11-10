# -*- coding: utf-8 -*-

'''
Por: Ángeles Blanco y Ana Rodríguez

Este script contiene una herencia de la clase MRJob que realiza el análisis de
sentimientos de un fichero de tweets, acorde al estudio AFINN. Además, ejecuta
un análisis de tendencia mediante las ocurrencias de 'hashtags'. El 'output' 
final es un ránking con los 10 primeros TTs (Trending Topic) junto al ránking 
de estados y felicidad.
'''

# Importamos librerías:
from mrjob.job import MRJob
from mrjob.step import MRStep
import json as js
import sys #para ver el fichero adicional situado en el directorio actual
sys.path.append('.') 
import re #definimos expresión regular para encontrar palabras
WORD_RE = re.compile(r"[\w]+") 
    
class tweetsentiment(MRJob):
    
    # Definimos pipeline de ejecución:
    def steps(self): 
        
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner_count,
                   reducer=self.reducer_count),
            MRStep(reducer=self.reducer_find_max)
            ]

    # Definimos mapper:
    def mapper(self, _, line):
        try:
            tweets = js.loads(line)
            text = tweets['text']
            lang = tweets['lang']
            place = tweets['place']
            if (place!= None) & (lang=="en"):
                place_type = place['place_type']
                # nos quedamos solo con estados de EEUU
                if (place['country_code']=='US') & (place_type=="admin"):
                    city = place['name']
                    
                    # Estados:
                    for word in WORD_RE.findall(text):
                        if word.lower() in scores:
                            yield city, scores[word]
                                                
                    # Hashtags:
                    if tweets['entities'] != None:
                        for hashtag in tweets['entities']['hashtags']:
                            yield ("#" + hashtag['text'].lower(), 1)
                                   
        except Exception: # en caso de que no se cumplan las condiciones
            pass            
    
    # Combinamos claves con sus distintos valores:
    def combiner_count(self, key, values):
        #sys.stderr.write("REDUCER INPUT: ({0},{1})\n".format(key,values))
        yield key, sum(values)

    # Sacamos recurrencia por cada hashtag y puntuaciones por cada estado:
    def reducer_count(self, key, values):
        
        # Agrupamos por campos comunes (hashtags y estados):
        if key.startswith("#"):
            yield 'hashtag', (key, sum(values))
        else:
            yield 'state', (key, sum(values))
    
    # Sacamos las divisiones estatales y los TT:
    def reducer_find_max(self, key, values):
        tt = []
        states = []
        n,n_ = 1,0
        
        # Ordenamos claves y valores:
        for occurrence in values:
            if key.startswith('hash'):
                tt.append(occurrence)
                tt.sort(reverse = True, key = lambda x: x[1])
                #tt = tt[:10]
            else:
                states.append(occurrence)
                states.sort(reverse = True, key = lambda x: x[1])
                
        # Sacamos TT con su orden en el ránking:
        for occurrence in tt[:10]:
            if n == 1: 
                yield str(n) + ' TT', occurrence
            else:
                if occurrence[1] == tt[n-2][1]:
                # si pertenecen al mismo puesto en el ránking
                    n_ = n_
                else:
                    n_ += 1
                yield str(n_+1) + ' TT', occurrence
            n += 1
        
        # Sacamos estados con su orden en el ránking:
        for occurrence in states:
            if n == 1:
                yield 'Happiest state', occurrence
            else:
                if occurrence[1] == states[n-2][1]:
                # si pertenecen al mismo puesto en el ránking
                    n_ = n_
                else:
                    n_ += 1
                yield str(n_+1) + ' rank', occurrence
            n += 1

if __name__ == '__main__':
    
    # Abrimos fichero de puntuaciones y lo guardamos en un diccionario:
    afinn = open("AFINN_111.txt")
    scores = {}
 
    for line in afinn: 
        term, score  = line.split("\t")  
        scores[term] = int(score) 
      
    # Llamamos a la ejecución de la clase:
    tweetsentiment.run()
    
