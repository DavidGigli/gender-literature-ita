with open("/home/masterbd/Documenti/PROGETTONE/libri_E","r") as opentesto:
	testo=opentesto.read()   #apro il documento con l'elenco dei libri che abbiamo

lst=testo.lower()

lst1=lst.split('.txt\n')

lista_finale = []

for el in lst1:
    tmp = el.split(",")
    if len(tmp)>=2:
        autore = tmp[0].split(" ")
        titolo = tmp[1]
        if len(autore)>=2:
            lista_finale.append([autore[0], autore[1], titolo])
        else:
            lista_finale.append([autore[0], titolo])
    else:
        autore = tmp[0].split(" ")
        if len(autore) >= 2:
            lista_finale.append([autore[0], autore[1]])
        else:
            lista_finale.append([autore[0]])

