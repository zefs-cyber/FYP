import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

opt = Options()
opt.add_argument('--headless')
driver = webdriver.Chrome(executable_path='C:\Users\dilovar.mashrabov\OneDrive - University of Central Asia\Desktop\s1\FYP\project\parsers\chromedriver.exe', chrome_options=opt)

def bonkirushd():
    url = 'https://brt.tj/ru/porteb'
    tags =[]

    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        tag = driver.find_elements(By.TAG_NAME, 'p')
        for i in tag:
            tags.append(i.get_attribute('innerHTML'))
        driver.close()
        driver.quit()

    r1 = int(''.join([b for b in tags[5].split('.')[2] if b.isnumeric()])[-4:])
    r2 = int(''.join([b for b in tags[6].split('.')[2] if b.isnumeric()])[:2])
    r3 = int(''.join([b for b in tags[7].split('.')[2] if b.isnumeric()])[:2])
    r4 = int(''.join([b for b in tags[9] if b.isnumeric()]))

    return [r3, r1*10, r4, r2, r1, r4]

def orienbank():
    url = 'https://orienbank.tj/individuals/loans/consumer'
    result =[]

    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        a = driver.find_elements(By.TAG_NAME, 'p')
        for i in a:
            content = ''.join([b for b in i.get_attribute('innerHTML') if b.isnumeric()])
            if len(content) != 0:
                result.append(content)
        driver.close()
        driver.quit()

    return [int(result[1]), int(result[0]), int(result[2][1:])]

def ssb():
    url = 'https://ssb.tj/credits/25?type=1'
    result =[]

    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        a = driver.find_elements(By.TAG_NAME, 'p')
        for i in a:
            content = ''.join([b for b in i.get_attribute('innerHTML') if b.isnumeric()])
            if len(content) != 0:
                result.append(content)
        driver.close()
        driver.quit()
        return [int(result[0]), int(result[1]), 24]

def arvand():
    url = 'https://www.arvand.tj/cl/kredity/potrebitelskiy'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('td'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)

    return [int(result[2][:2]), int(result[0]), int(result[1]), int(result[2][-2:]), int(int(result[0])/10), int(result[1])]

def amonatbank():  
    url = 'https://www.amonatbonk.tj/en/personal/loans/potrebitelskiy-kredit/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('h3'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)

    return [int(result[2]), int(result[0]), int(result[1])]

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

def eskhata():
    url = 'https://eskhata.com/individuals/lending/lending_types/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

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

def spitamen():
    url = 'https://www.spitamenbank.tj/ru/products/personal/credit/potrebitelskie-kredity/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('td'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)

    return [int(result[2]), int(result[0][-5:]), int(result[4][-2:]), int(result[3]), int(result[1][-4:]), int(result[4][-2:])]

    url = 'https://ssb.tj/credits/25?type=1'
    result =[]
    driver = webdriver.Chrome(executable_path='parsers\chromedriver.exe')

    try:
        driver.get(url=url)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        a = driver.find_elements(By.TAG_NAME, 'p')
        for i in a:
            content = ''.join([b for b in i.get_attribute('innerHTML') if b.isnumeric()])
            if len(content) != 0:
                result.append(content)
        driver.close()
        driver.quit()
        return [int(result[0]), int(result[1]), 24]



parsers = [orienbank, amonatbank, eskhata, bonkirushd, arvand, spitamen, ibt, cbt, ssb]

for i in parsers:
    print(i())