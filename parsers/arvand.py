import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def arvand():
    url = 'https://www.arvand.tj/cl/kredity/potrebitelskiy'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    c = 1
    result = []
    for i in soup.find_all('td'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            print(str(c) + " : " + content)
            c += 1
            result.append(content)

    return [int(result[2][:2]), int(result[0]), int(result[1]), int(result[2][-2:]), int(int(result[0])/10), int(result[1])]