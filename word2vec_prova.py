import urllib.request
import os
import re
import multiprocessing
from gensim.models import Phrases
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import CountVectorizer
from nomi_propri import*
import copy

file_testo = open("/home/masterbd/progetto/CONVERTITI_UTF8/Giordano Paolo,La solitudine dei numeri primi.txt",'r')#definisco una variabile contenente la funzione di apertura in modalità lettura del testo (il path va tra virgolette se no dà errore)
testo = file_testo.read() #trasformo il contenuto del file in testo con il metodo '.read'.
testo = testo[testo.find('1\n'):]
testo_norm = testo.split('.\n')
print(testo_norm[0])
sentences_w2v=[]

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

analyzer = CountVectorizer(token_pattern='(?u)\\b\\w+\\b').build_analyzer()

#con la funzione di sopra costruiamo la lista di liste da dare al word2vec partendo da una lista di
#stringhe che l'analyzer parsa e ne filtra i caratteri non alfabetici
sentences_w2v_1 = prepareListofStr(testo_norm, analyzer)
print(sentences_w2v_1)

#vogliamo sostituire i nomi propri di persona maschili e femminili con due parole inventate
##creiamo le due liste di nomi maschili e femminili
nomi_femminili=set(lista_nomi("/home/masterbd/progetto/nomi_femminili.csv"))
nomi_maschili=set(lista_nomi("/home/masterbd/progetto/nomi_maschili.csv"))
##
print('operazioni sui nomi fatte')

##confronto ogni parola del testo con ogni parola nella lista dei nomi
sentences_w2v = copy.copy(sentences_w2v_1)
for i, paragrafo in enumerate(sentences_w2v):
    for j, parola in enumerate(paragrafo):
        if parola in nomi_femminili:
            #print('nome_femminile: ',parola)
            sentences_w2v[i][j] = 'GuneGunaikos'
        elif parola in nomi_maschili:
            #print('nome_maschile: ', parola)
            sentences_w2v[i][j] = 'AnerAndros'
print('sostituzione alias nomi fatto')
print('creazione word2vect')

libri2vecpath = './libri2vec'
#generateEmbeddings(sentences, libri2vecpath, window=1, ngrams=2, min_count=1)
#fare qui le modifiche ai parametri
model = Word2Vec(sentences_w2v, min_count=1, iter=50)#iter è il numero di iterazioni: se il testo di training è già molto lungo, bastano 5 iterazioni
model.save(libri2vecpath)
model = Word2Vec.load(libri2vecpath)
vec = model.wv['GuneGunaikos']
#print('stampo vettori')
#print(vec)

#chiediamo qual è il più simile
print('i più simili')
print(model.most_similar('GuneGunaikos',topn=20)) #prende i 20  migliori
