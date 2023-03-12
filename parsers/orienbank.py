import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

def orienbank():
    url = 'https://orienbank.tj/individuals/loans/consumer'
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

    return [int(result[1]), int(result[0]), int(result[2][1:])]