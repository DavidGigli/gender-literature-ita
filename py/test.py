import json
from urllib.parse import urlencode
from urllib.request import urlopen
import re
from sys import stdout  # questo import serve per l'estetica, ovvero per stampare la percentuale di avanzamento
import os
API_URL="https://it.wikipedia.org/w/api.php"

def page_exists(title):  # funzione che ritorna -1 se la pagina non esiste, altrimenti ritorna il page_id della pagina.
    data = {"action": "query", "prop": "revisions", "rvlimit": 1, "rvprop": "content", "format": "json","titles": title}
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
    # pattern = r"\{\{(.*?)\}\}|$"
    matches = pagina_wiki(bio_nome)
    re_epoca = r"\|Epoca = (.*)"
    ricerca_epoca = re.search(re_epoca, matches)
    if ricerca_epoca is None:
        epoca = "-1"
    else:
        epoca = ricerca_epoca.group(1)

    re_naz = r"\|Attività = (.*)"
    ricerca_nazionalità = re.search(re_naz, matches)
    if ricerca_nazionalità is None:
        nazionalità = "Non pervenuta"
    else:
        nazionalità = ricerca_nazionalità.group(1)
    return {'Epoca': epoca, 'Nazionalità': nazionalità}

print(pagina_wiki("Carlo Botta"))
print(epoca_naz_wiki("Giovanni Bovio"))
