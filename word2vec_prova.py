import urllib.request
import os
import re
import multiprocessing
from gensim.models import Phrases
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer
file_testo = open("/media/laura/TOSHIBA/romanzi_contemporanei_convertiti_utf8/autori/Giordano Paolo,La solitudine dei numeri primi.txt",'r')#definisco una variabile contenente la funzione di apertura in modalità lettura del testo (il path va tra virgolette se no dà errore)
testo = file_testo.read() #trasformo il contenuto del file in testo con il metodo '.read'.
testo = testo[testo.find('1\n'):]
testo_norm = testo.split('.\n')
print(testo_norm[0])
#non modificare qui questi parametri, modificali nel main
def generateEmbeddings(sentences, outputFile, size=100, window=5, min_count=10, ngrams=0):
    for n in range(ngrams - 1):
        bigram_transformer = Phrases(sentences, min_count=min_count)
        sentences = bigram_transformer[sentences]
        print(sentences)
        #sentences = bigram_transformer[n]
    model = Word2Vec(sentences, size=size, window=window, min_count=min_count,
                     workers=multiprocessing.cpu_count() ) #, hashfxn=hash32)
    model.init_sims(replace=True)
    model.save(outputFile)
#una funzione che partendo da una lista di stringhe con l'analyzer fa il parsing e crea una lista
#di liste
def prepareListofStr(list_of_str, analyzer):
    return [analyzer(str) for str in list_of_str]
#una funzione che partendo da una lista di stringhe con l'analyzer fa il parsing e crea una lista
#di liste
def prepareListofStr(list_of_str, analyzer):
    return [analyzer(str) for str in list_of_str]

analyzer = CountVectorizer(token_pattern='(?u)\\b\\w+\\b').build_analyzer()
#con la funzione di sopra costruiamo la lista di liste da dare al word2vec partendo da una lista di
#stringhe che l'analyzer parsa e ne filtra i caratteri non alfabetici
sentences_w2v = prepareListofStr(testo_norm, analyzer)
print(sentences_w2v)
libri2vecpath = './libri2vec'
#generateEmbeddings(sentences, libri2vecpath, window=1, ngrams=2, min_count=1)
#fare qui le modifiche ai parametri
model = Word2Vec(sentences_w2v, min_count=1, iter=50)#iter è il numero di iterazioni: se il testo di training è già molto lungo, bastano 5 iterazioni
model.save(libri2vecpath)
model = Word2Vec.load(libri2vecpath)
vec = model.wv['alice']
print(vec)
#chiediamo qual è il più simile
print(model.most_similar('alice'))
