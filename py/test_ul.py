# import time
from selenium import webdriver

chromeOptions = webdriver.ChromeOptions()
path_dest = "/home/masterbd/progetto/liber_liber"
prefs = {"download.default_directory" : path_dest}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get('https://www.liberliber.it/online/autori/autori-d/gabriele-dannunzio/')
elencolibri = driver.find_elements_by_xpath("//ul//li[@class='ll_autore_elenco_libro']//span[@class='ll_autore_elenco_opera_titolo']//a")
link_libri = []
for elem in elencolibri:
    link = elem.get_attribute("href")
    link_libri.append(link)
print(link_libri)
