import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def eskhata():
    url = 'https://eskhata.com/individuals/lending/lending_types/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    c = 1
    result1 = []
    for i in soup.find_all('p', class_ = 'MsoNormal'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result1.append(content)

    result2 = []
    for i in soup.find_all('li'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result2.append(content)

    return [int(result2[3][-2:]), int(result1[0]), int(result1[1])]