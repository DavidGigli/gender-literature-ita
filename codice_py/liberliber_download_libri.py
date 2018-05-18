import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "/home/masterbd/progetto/liber_liber"}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
driver.get('https://www.liberliber.it/online/autori/autori-d/gabriele-dannunzio/alcione/')
time.sleep(1)
try:
    link_libro = driver.find_element_by_class_name("ll_ebook_txtzip_free")
except NoSuchElementException:
    try:
        link_libro = driver.find_element_by_class_name("ll_ebook_htmlzip_free")
    except NoSuchElementException:
        try:
            link_libro = driver.find_element_by_class_name("ll_ebook_odt_free")
        except NoSuchElementException:
            link_libro = "NIENTE"
if link_libro != "NIENTE":
    nome_file = link_libro.find_element_by_xpath("..").get_attribute("href").split("/")[-1]
    print(test)
    #link_libro.click()
    time.sleep(1)
driver.quit()
