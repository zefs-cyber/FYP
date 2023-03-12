import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def ibt():
    url = 'https://ibt.tj/credits/kredit-na-neobkhodimye-nuzhdy/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []

    for i in soup.find_all('td'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)

    return [int(result[2][-2:]), int(result[0][-5:]), int(result[1][-2:]), int(result[2][-4:-2]), int(int(result[0][-5:])/10), int(result[1][-2:])]

