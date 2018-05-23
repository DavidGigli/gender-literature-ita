from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.goodreads.com/review/show/2328459500')
testo = driver.find_element_by_xpath("//div[@itemprop='reviewBody']")
print(testo.text)
driver.quit()
