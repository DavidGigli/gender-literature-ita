import json
from urllib.parse import urlencode
from urllib.request import urlopen
import re
from sys import stdout  # questo import serve per l'estetica, ovvero per stampare la percentuale di avanzamento
import os
API_URL="https://it.wikipedia.org/w/api.php"

def page_exists(title):  # funzione che ritorna -1 se la pagina non esiste, altrimenti ritorna il page_id della pagina.
    data = {"action": "query", "prop": "revisions", "rvlimit": 1, "rvprop": "content", "format": "json",
            "titles": title}
    raw = urlopen(API_URL, urlencode(data).encode()).read()
    res = json.loads(raw.decode('utf-8'))
    page_id = next(iter(res["query"]["pages"]))
    return page_id

def pagina_wiki(title):
    data = {"action": "query", "prop": "revisions", "rvlimit": 1, "rvprop": "content", "format": "json",
            "titles": title}
    raw = urlopen(API_URL, urlencode(data).encode()).read()
    res = json.loads(raw.decode('utf-8'))
    text = res["query"]["pages"][page_exists(title)]["revisions"][0]["*"]
    return text


def epoca_naz_wiki(bio_nome):
	matches = pagina_wiki(bio_nome)
	re_epoca = r"\|Epoca = (.*)"
	ricerca_epoca = re.search(re_epoca, matches)
	if ricerca_epoca is None:
		epoca = "-1"
	else:
		epoca = ricerca_epoca.group(1)
	re_naz = r"\|Nazionalità = (.*)"
	ricerca_nazionalità = re.search(re_naz, matches)
	if ricerca_nazionalità is None:
		nazionalità = "Non pervenuta"
	else:
		nazionalità = ricerca_nazionalità.group(1)
	re_nasc = r"\|AnnoNascita = (.*)"
	ricerca_nascita = re.search(re_nasc, matches)
	if ricerca_nascita is None:
		nascita = "-1"
	else:
		nascita = ricerca_nascita.group(1)
	re_morte = r"\|AnnoMorte = (.*)"
	ricerca_morte = re.search(re_morte, matches)
	if ricerca_morte is None:
		morte = "-1"
	else:
		morte = ricerca_morte.group(1)
	re_sesso = r"\|Sesso = (.*)"
	ricerca_sesso = re.search(re_sesso, matches)
	if ricerca_sesso is None:
		sesso = "non trovato"
	else:
		sesso = ricerca_sesso.group(1)
	re_luogo = r"\|LuogoNascita = (.*)"
	ricerca_luogo = re.search(re_luogo, matches)
	if ricerca_luogo is None:
		luogo = "non trovato"
	else:
		luogo = ricerca_luogo.group(1)
	
	return {'Epoca':epoca, 'Nazionalità':nazionalità, 'Nascita':nascita,'Morte':morte, 'Sesso':sesso,'Luogo_Nascita':luogo}
	
###per far girare lo script su uno a scelta dei tre files
#nome_file="autori_a_z.txt"          # questo file è quello che viene generato dallo scraping di liberliber
#nome_file="autori_titoli_cnr.txt"   # elenco libri del CNR
nome_file="elenco_libri.txt"        # elenco libri di Esuli
#suffisso="liber"
#suffisso="cnr"
suffisso="esuli"

elenco=os.path.join("/home/masterbd/progetto/",nome_file)
aut_wiki=os.path.join("/home/masterbd/progetto/","autori+wiki_"+suffisso+".txt")
aut_mancanti=os.path.join("/home/masterbd/progetto/","autori_mancanti_"+suffisso+".txt")

lista_autori = open(elenco,"r").readlines()
lista_aut_wiki = open(aut_wiki,"r")  # deve esistere un file con questo nome in cui andrà la lista degli autori presenti su wikipedia
lista_mancanti = open(aut_mancanti,"r")  # deve esistere un file con questo nome in cui andranno gli autori NON presenti su wikipedia
lis_wiki = lista_aut_wiki.readlines()
lis_man = lista_mancanti.readlines()
ind_aut_pres = len(lis_wiki) - 1
ind_aut_ass = len(lis_man)
set_of_aut=set() #insieme degli autori visti, così non si fanno ricerche duplicate
for line in lis_wiki:
	aut_visto = line.split("|")[0].strip()	
	set_of_aut.add(aut_visto)
for aut_man in lis_man:
	set_of_aut.add(aut_man.strip())
lista_aut_wiki.close()

if len(lis_wiki) == 0:
    lista_aut_wiki = open(aut_wiki, "w")
    lista_aut_wiki.write("Nome e Cognome|Cognome, Nome (originale)|Wiki Page_id|Epoca|Nazionalità|AnnoNascita|AnnoMorte|Sesso|Luogo_Nascita\n")
    lista_aut_wiki.close()
lista_aut_wiki = open(aut_wiki, "a")
lista_mancanti = open(aut_mancanti, "a")
riga_partenza = ind_aut_pres + ind_aut_ass
num_tot_aut = len(lista_autori)
for i, line in enumerate(lista_autori):
    if i < riga_partenza:
        continue
    valore_orig = line.split("|")[0]
    autore = line.split("|")[0].split(",")
    autore.reverse()
    autore = re.sub(' +', ' ', " ".join(autore).strip(' '))
    if autore not in set_of_aut:
        exists = page_exists(autore)  # è -1 se la pagina non esiste
        set_of_aut.add(autore)
        if int(exists) > 0:
            pagina_wiki(autore)
            stringa=autore + "|" + valore_orig + "|" + exists + "|" + epoca_naz_wiki(autore)["Epoca"] + "|" + epoca_naz_wiki(autore)["Nazionalità"] + "|" + epoca_naz_wiki(autore)["Nascita"] + "|" + epoca_naz_wiki(autore)["Morte"] + "|" + epoca_naz_wiki(autore)["Sesso"] + "|" + epoca_naz_wiki(autore)["Luogo_Nascita"] + "\n"
            lista_aut_wiki.write(stringa)
        else:
            lista_mancanti.write(autore + "\n")
    stdout.write("\rControllate {} linee, siamo al {:.0%} del processo".format(riga_partenza,riga_partenza / num_tot_aut))  # serve per scrivere il risultato nella stessa riga
    stdout.flush()
    riga_partenza += 1
stdout.write("\n")  # Sposta il cursore sulla nuova linea alla fine del ciclo (ovvero del programma) altrimenti sovrascriverebbe l'ultima linea.
lista_aut_wiki.close()
lista_mancanti.close()
