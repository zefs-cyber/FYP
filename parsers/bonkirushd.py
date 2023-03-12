import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def bonkirushd():
    url = 'https://brt.tj/ru/porteb'
    tags =[]
    driver = webdriver.Chrome(executable_path='parsers\chromedriver.exe')
    counter = 1
    try:
        driver.get(url=url)
        time.sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        a = driver.find_elements(By.TAG_NAME, 'p')
        for i in a:
            tags.append(i.get_attribute('innerHTML'))
            counter += 1
        driver.close()
        driver.quit()



    r1 = int(''.join([b for b in tags[5].split('.')[2] if b.isnumeric()])[-4:])
    r2 = int(''.join([b for b in tags[6].split('.')[2] if b.isnumeric()])[:2])
    r3 = int(''.join([b for b in tags[7].split('.')[2] if b.isnumeric()])[:2])
    r4 = int(''.join([b for b in tags[9] if b.isnumeric()]))

    return [r3, r1*10, r4, r2, r1, r4]