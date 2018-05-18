from goodreads import client
import time
import csv

Path="/home/masterbd/Python/progetto/libri_goodreads.csv"
file_libri = open(Path,'r+')
gc = client.GoodreadsClient("powmxLHGknXL5rj5cEKN2w","IQWIEtmYaaVN3ADY1cx4qKBjWQ2DfyLUqsA2c")
id_book=1
file_writer=csv.writer(file_libri, delimiter=',')
while id_book<100:
	book = gc.book(id_book)
	print(book.title)
	authors = book.authors
	print(authors[0])
	time.sleep(1)
	riga=[]
	riga.append(id_book)
	riga.append(book)
	riga.append(authors)
	file_writer.writerow(riga)
	id_book += 1
file_writer.close()

