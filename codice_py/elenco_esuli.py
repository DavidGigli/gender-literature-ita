with open("/home/masterbd/progetto/libri","r") as opentesto:
	testo=opentesto.read()   #apro il documento con l'elenco dei libri che abbiamo
file_autori = open("/home/masterbd/progetto/elenco_libri.txt","w")

#lst=testo.lower()
lst1=testo.split('.txt\n')
lista_finale = []

for el in lst1:
    tmp = el.split(",")
    if len(tmp)>=2:
        autore = tmp[0].split(" ")
        titolo = tmp[1]
        if len(autore)>=2:
            lista_finale.append([autore[0], autore[1], titolo])
            stringa=autore[0]+", "+autore[1]+"|"+titolo+"\n"
        else:
            lista_finale.append([autore[0], titolo])
            stringa = autore[0]  + "|" + titolo+"\n"
    else:
        autore = tmp[0].split(" ")
        if len(autore) >= 2:
            lista_finale.append([autore[0], autore[1]])
            stringa = autore[0] + ", " + autore[1] + "|" +"\n"
        else:
            lista_finale.append([autore[0]])
            stringa =autore[0]+"\n"
    file_autori.write(stringa)

file_autori.close()                            #chiudo il file su cui ho scritto il nuovo elenco di autori  con cognome e nome

