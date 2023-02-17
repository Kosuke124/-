from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests
import urllib.request as req
from webdriver_manager.chrome import ChromeDriverManager
kaigiID=2021020134208001

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("http://www.kensakusystem.jp/ayabe/cgi-bin3/ResultFrame.exe?Code=miwbm3vtn01wqft84u&fileName=H280906A&startPos=0")

iframe = driver.find_element_by_name('TEXTW')
driver.switch_to.frame(iframe)
iframe = driver.find_element_by_name('TEXTREFS')
driver.switch_to.frame(iframe)

btn=driver.find_element_by_xpath('/html/body/table[1]/tbody/tr[1]/td[4]/a')
btn.click()

driver.switch_to.default_content()
iframe = driver.find_element_by_name('TEXTW')
driver.switch_to.frame(iframe)
iframe = driver.find_element_by_name('TEXT0')
driver.switch_to.frame(iframe)

source = BeautifulSoup(driver.page_source, "html.parser").prettify()
soup = BeautifulSoup(source, "html.parser")

tex=soup.find(class_='TEXT2').text
print(tex)
hatugen = tex.split('○')

for i in range(len(hatugen)):
    hatugen[i] = hatugen[i].split()

driver.quit()