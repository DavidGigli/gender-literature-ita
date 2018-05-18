from goodreads import client
from selenium import webdriver
import time
import csv
#driver = webdriver.Chrome()
#driver.get('https://www.goodreads.com/review/show/2328459500')
#testo = driver.find_element_by_xpath("//div[@itemprop='reviewBody']")
#print(testo.text)

Path="/home/masterbd/Python/progetto/libri_goodreads.csv"
file_libri = open(Path,'r+')
gc = client.GoodreadsClient("powmxLHGknXL5rj5cEKN2w","IQWIEtmYaaVN3ADY1cx4qKBjWQ2DfyLUqsA2c")
next_book=1
file_writer=csv.writer(file_libri, delimiter=',')
while next_book<100:
	book = gc.book(next_book)
	print(book.title)
	authors = book.authors
	print(authors[0])
	time.sleep(1)
	riga=[]
	riga.append(next_book)
	riga.append(book)
	riga.append(authors)
	file_writer.writerow(riga)
	next_book += 1
file_writer.close()
#driver.quit()
