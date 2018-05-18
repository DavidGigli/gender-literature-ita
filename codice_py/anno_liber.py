#ls lista path libri
#per ogni libro lo apro. read()
#dentro la stringa cerco tra "tratto da: " e "codice ISBN"
#diff tra numero di file e numero di risultati

from os import listdir
from os.path import isfile, join
import re

path_dest = "/home/masterbd/progetto/convertiti/"
list_file_libri = [path_dest+f for f in listdir(path_dest) if isfile(join(path_dest, f))] #lista dei nomi dei file nella cartella
pattern = r"tratto da:(.*)1a edizione elettronica"
n_risultati = 0

for libro in list_file_libri:
	with open(libro,"r") as mylibro:
		stringa=mylibro.read().lower()
		#print(stringa)
		risultato = re.search(pattern, stringa, re.DOTALL)
		if risultato is None:
			ris = "0"
		else:
			ris= risultato.group(1)
			num_4 = re.findall(r"[^\d][12]\d\d\d[^\d]", ris)[-1]
			n_risultati += 1
			if num_4 is None:
				anno = 1000
			else:
				anno = num_4[1:-1]
		print(libro, anno)
		
print(len(list_file_libri) - n_risultati)
print(len(list_file_libri))

#più o meno ci siamo
