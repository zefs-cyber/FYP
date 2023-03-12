import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def cbt():
    url = 'https://cbt.tj/retail/credits/barakat'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('div', class_ = 'col-md-9'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)
    return [int(result[1][-2:]), int(result[0]), int(result[2])]
    
