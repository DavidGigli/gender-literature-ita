#cose da fare:
#set dei file nella cartella di destinazione (done)
#lista degli autori da scaricare (done)
#dalla lista dei link check se l'autore è da scaricare (done)
#ciclo sugli elementi dell'elenco (done)
#check prima del download se il file è già nel set o meno
#download
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from os import listdir
from shutil import copyfile
from os.path import isfile, join

# def newest(path):
#    files = listdir(path)
#    paths = [join(path, basename) for basename in files]
#    return max(paths, key=os.path.getctime)

chromeOptions = webdriver.ChromeOptions()
path_down = "/home/masterbd/progetto/workspace/"
path_dest = "/home/masterbd/progetto/liber_liber/"
prefs = {"download.default_directory" : path_down}
chromeOptions.add_experimental_option("prefs",prefs)

set_file_libri = {f for f in listdir(path_down) if isfile(join(path_down, f))} #set dei nomi dei file nella cartella

in_autori = open("/home/masterbd/progetto/autori+wiki_finito.txt","r").readlines()
in_url = open("/home/masterbd/progetto/autori_a_z.txt","r").readlines()
scaricati = open("/home/masterbd/progetto/liber_liber/LINK_SCARICATI","r").readlines()
elenco_scaricati = set()
for line in scaricati:
    elenco_scaricati.add(line.strip())
set_aut_down = set()
set_aut_gia_sca = set()
file_aut_scar = open("/home/masterbd/progetto/liber_liber/AUTORI_SCARICATI","r").readlines()
for line in file_aut_scar:
    set_aut_gia_sca.add(line.strip())

for i, line in enumerate(in_autori):
    if i == 0:
        print("prima linea, skippata")
        continue
    content = line.split("|")
    epoca = int(content[3].strip())
    nazionalita = content[4].strip()
    if epoca > 1799 and (nazionalita == "italiano" or nazionalita == "italiana"):
        set_aut_down.add(content[1].strip())
set_aut_down = set_aut_down - set_aut_gia_sca
scaricati_scri = open("/home/masterbd/progetto/liber_liber/LINK_SCARICATI","a")
file_aut = open("/home/masterbd/progetto/liber_liber/AUTORI_SCARICATI","a")
file_nomi_libri = open(path_down+"libri_link_nomi","a")
for i, line in enumerate(in_url):
    nome = line.split("|")[0].strip()
    url_aut = line.split("|")[1].strip()
    link_libri = []
    if i % 20 == 0:
        driver = webdriver.Chrome(chrome_options=chromeOptions)
    if nome in set_aut_down:
        driver.get(url_aut)
        #time.sleep(1)
        elencolibri = driver.find_elements_by_xpath("//ul//li[@class='ll_autore_elenco_libro']//span[@class='ll_autore_elenco_opera_titolo']//a")
        for elem in elencolibri:
            link = elem.get_attribute("href")
            link_libri.append(link)
    for url in link_libri:
        if url in elenco_scaricati:
            continue
        else:
            scaricati_scri.write(url+"\n")
            driver.get(url)
            nome_finale = driver.find_element_by_class_name("entry-title").text
            print(nome_finale)
            try:
                link_libro = driver.find_element_by_class_name("ll_ebook_txtzip_free")
            except NoSuchElementException:
                try:
                    link_libro = driver.find_element_by_class_name("ll_ebook_htmlzip_free")
                except NoSuchElementException:
                    try:
                        link_libro = driver.find_element_by_class_name("ll_ebook_odt_free")
                    except NoSuchElementException:
                        try:
                            link_libro = driver.find_element_by_class_name("ll_ebook_epub_free")
                        except NoSuchElementException:
                            link_libro = "NIENTE"
                            continue
            if link_libro != "NIENTE":
                nome_file = link_libro.find_element_by_xpath("..").get_attribute("href").split("/")[-1]
                if nome_file not in set_file_libri:
                    link_libro.click()
#                    exists = False
                    time.sleep(1)
                file_nomi_libri.write(nome_file + "|" + nome + " - " + nome_finale+"\n")
    #                    while not exists:
#                        if newest(path_down).split(".")[-1] != "crdownload":
#                            exists = True
                    #estensione = nome_file.split(".")[-1]
                    #copyfile(path_down+nome_file,path_dest+nome+" - "+nome_finale+"."+estensione)
    file_aut.write(nome+"\n")

    if i % 20 == 19:
        driver.quit()
file_aut.close()
scaricati_scri.close()
driver.quit()