import json
from urllib.parse import urlencode
from urllib.request import urlopen
import re
from sys import stdout  # questo import serve per l'estetica, ovvero per stampare la percentuale di avanzamento
import os

API_URL = "https://it.wikipedia.org/w/api.php"


def page_exists(title):  # funzione che ritorna -1 se la pagina non esiste, altrimenti ritorna il page_id della pagina.
    data = {"action": "query", "prop": "revisions", "rvlimit": 1, "rvprop": "content", "format": "json",
            "titles": title}
    raw = urlopen(API_URL, urlencode(data).encode()).read()
    res = json.loads(raw)
    page_id = next(iter(res["query"]["pages"]))
    return page_id


def pagina_wiki(title):
    data = {"action": "query", "prop": "revisions", "rvlimit": 1, "rvprop": "content", "format": "json",
            "titles": title}
    raw = urlopen(API_URL, urlencode(data).encode()).read()
    res = json.loads(raw)
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
    re_attività = r"\|Attività = (.*)"
    ricerca_attività = re.search(re_attività, matches)
    if ricerca_attività is None:
        attività1 = "non trovata"
    else:
        attività1 = ricerca_attività.group(1)
    re_attività2 = r"\|Attività2 = (.*)"
    ricerca_attività2 = re.search(re_attività2, matches)
    if ricerca_attività2 is None:
        attività2 = "non trovata"
    else:
        attività2 = ricerca_attività2.group(1)

    return {'Epoca': epoca, 'Nazionalità': nazionalità, 'Nascita': nascita, 'Morte': morte, 'Sesso': sesso,
            'Luogo_Nascita': luogo, 'Attività1': attività1, 'Attività2': attività2}


nome_file = "autori+wiki_liber.txt"  # elenco autori di Esuli

elenco = os.path.join("/home/masterbd/progetto/", nome_file)

file_out = open("/home/masterbd/progetto/attivita_autori_liber.txt","w")

lista_autori = open(elenco, "r").readlines()
set_of_aut = set()  # insieme degli autori visti, così non si fanno ricerche duplicate

num_tot_aut = len(lista_autori)
for i, line in enumerate(lista_autori):
    line = line.strip()
    linea_spezzata = line.split("|")
    autore = linea_spezzata[0].strip()
    nazionalità = linea_spezzata[4].strip()
    try:
        epoca = int(linea_spezzata[3].strip())
    except ValueError:
        epoca = 0
    if epoca > 1799 and (nazionalità == "italiano" or nazionalità == "italiana"):
        if autore not in set_of_aut:
            exists = page_exists(autore)  # è -1 se la pagina non esiste
            set_of_aut.add(autore)
            if int(exists) > 0:
                stringa = line + "|" + epoca_naz_wiki(autore)["Attività1"] + "|" + epoca_naz_wiki(autore)["Attività2"] + "\n"
            else:
                stringa = line + "|" + "manca" + "|" + "manca" "\n"
            file_out.write(stringa)
    stdout.write("\rControllate {} linee, siamo al {:.0%} del processo".format(i,i/ num_tot_aut))  # serve per scrivere il risultato nella stessa riga
    stdout.flush()
stdout.write("\n")  # Sposta il cursore sulla nuova linea alla fine del ciclo (ovvero del programma) altrimenti sovrascriverebbe l'ultima linea.
file_out.close()
