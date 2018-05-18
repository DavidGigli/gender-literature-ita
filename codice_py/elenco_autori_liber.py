import time
import string
from selenium import webdriver

driver = webdriver.Chrome()
file_autori = open("/home/masterbd/progetto/autori_a_z.txt","w")
for lettera in string.ascii_lowercase:
	driver.get('https://www.liberliber.it/online/autori/autori-'+lettera)
	elenco_autori = driver.find_elements_by_css_selector("ul")[35] #il 35 va messo perché ci sono un sacco di ul nel file html
	autori = elenco_autori.find_elements_by_css_selector("li")
	for autore in autori:
		stringa=autore.text + " | " + autore.find_element_by_css_selector("a").get_attribute("href") + "\n"
		file_autori.write(stringa)
file_autori.close()
driver.quit()
