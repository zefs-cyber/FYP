import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from openpyxl import Workbook
import time
import pandas as pd

opt = Options()
opt.add_argument('--headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)

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

    return [int(result[1]), int(result[0]), int(result[2][1:])]

def ssb():

    url = 'https://www.ssb.tj/credits?type=1'
    result =[]

    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        p = driver.find_elements(By.TAG_NAME, 'p')
        for i in p:
            # content = ''.join([b for b in i.get_attribute('innerHTML') if b.isnumeric()])
            content = i.get_attribute('innerHTML')
            print(content)
            if content.isnumeric():
                result.append(int(content))

        return result 
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

    return [int((int(result[2][:2])+int(result[2][2:4]))/2), int(result[0]), int(result[1]), int((int(result[2][4:6])+int(result[2][6:8]))/2), int(int(result[0])/10), int(result[1])]

def amonatbank():  
    url = 'https://www.amonatbonk.tj/en/personal/loans/potrebitelskiy-kredit/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result1 = []
    for i in soup.find_all('h3'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result1.append(content)
    
    result2 = []
    for i in soup.find_all('p'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result2.append(content)
    
    return [int(result1[2]), int(result1[0]), int(result1[1]), int(result2[3]), int(int(result1[0])/10), int(result1[1])]

def cbt():
    url = 'https://cbt.tj/retail/credits/barakat'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('div', class_ = 'col-md-9'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)
    
    return [int(result[1][:2]), int(result[0][10:-1]), int(result[2]), int(result[1][6:8]), int(int(result[0][10:-1])/10), int(result[2])]

def eskhata():
    url = 'https://eskhata.com/individuals/lending/lending_types/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")


    result = []
    for i in soup.find_all('li'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)

    return [int(result[3][:2]), int(result[4][4:]), int(result[5])]

def ibt():
    url = 'https://ibt.tj/credits/kredit-na-neobkhodimye-nuzhdy/'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result = []
    for i in soup.find_all('td'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result.append(content)
    # return result
    return [int(result[2][-2:])+1, int(result[0]), int(result[1][-2:]), int(result[2][:2])-1, int(int(result[0])/10), int(result[1][-2:])]

def spitamen():
    url = 'https://www.spitamenbank.tj/ru/personal/products/credits/potrebitelskiy-kredit'

    site = requests.get(url)
    soup = BeautifulSoup(site.text, "html.parser")

    result_div = []
    for i in soup.find_all('div', class_='sb-quest'):
        content = ''.join([b for b in i.text if b.isnumeric()])
        if content != '':
            result_div.append(content)
    
    result_h3 = [''.join([b for b in i.text if b.isnumeric()]) for i in soup.find_all('h3') if ''.join([b for b in i.text if b.isnumeric()])!='']

    # return result_div, result_h3
    return [int(result_h3[0]), int(result_h3[2]), int(result_h3[1]), int(result_div[1][4:6]), int(result_h3[2])/10, int(result_h3[1])]

def update():
    parsers = {
        0:('Orienbank',orienbank),                     
        1:('Amonatbank',amonatbank),                   
        2:('Eskhata Bank',eskhata),                    
        8:('Bank "Arvand"',arvand),                    
        5:('Bonki Rushdi Tojikiston',bonkirushd),      
        9:('Spitamen Bank',spitamen),                   
        10:('International Bank of Tajikistan',ibt),  
        11:('Commerce Bank of Tajikistan',cbt),       
        # 13:('Sanoatsodirotbonk',ssb),                 
    }
    results = {}
    for i in parsers.keys():
        try:
            result = parsers[i][1]()
            if len(result) > 0:
                results[i] = result
        except Exception as e:
            with open('log.txt', 'a') as file:
                file.write(f'\n{e}')
    driver.close()
    driver.quit()

    
    df = pd.read_excel('loan_data.xlsx', 'consumer loan', engine='openpyxl').set_index('Bank id')
    df1 = pd.read_excel('loan_data.xlsx', 'car loan', engine='openpyxl').set_index('Bank id')
    df2 = pd.read_excel('loan_data.xlsx', 'data presence', engine='openpyxl').set_index('Bank id')
    for i in results.keys():
        names = ['%TJS', 'maxTJS', 'durationTJS', '%USD', 'maxUSD', 'durationUSD']
        if df.at[i, 'USD']:
            for name in range(6):
                df.at[i,names[name]] = results[i][name] 
        else:
            for name in range(3):
                df.at[i,names[name]] = results[i][name]
    
    with pd.ExcelWriter('loan_data copy.xlsx') as writer:
        df2.to_excel(writer, sheet_name='data presence', index=True)
        df1.to_excel(writer, sheet_name='car loan', index=True)
        df.to_excel(writer, sheet_name='consumer loan', index=True)

def fill_amonatbank(test):
    url = 'https://www.amonatbonk.tj/en/personal/loans/potrebitelskiy-kredit/#formCredit'
    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        inputName = driver.find_element(By.ID, "name")
        inputName.send_keys(test[0])
        inputNumber = driver.find_element(By.ID, "number_phone")
        inputNumber.send_keys(test[1])
        inputAmount = driver.find_element(By.ID, "sum")
        inputAmount.send_keys(test[2])
        inputFile = driver.find_element(By.ID, "file-foto")
        inputFile.send_keys(test[3])

        send = driver.find_element(By.ID, 'send_loan')
        send.click()

        driver.close()
        driver.quit()

def fill_cbt(test):
    url = 'https://cbt.tj/retail/credits/barakat'

    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        btn1 = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div/a')
        btn1.click()

        continue_btns = driver.find_elements(By.CLASS_NAME, '_credit_continue')
        time.sleep(1)

        continue_btns[0].click()
        time.sleep(1)

        continue_btns[1].click()
        time.sleep(1)

        inputSumm = driver.find_element(By.ID, '_credit_sum')   
        inputCurrency = Select(driver.find_element(By.ID, '_credit_currency'))
        inputReason = Select(driver.find_element(By.ID, '_credit_purpose'))

        if test[0] == 'tjs':
            inputCurrency.select_by_value('1')
        else:
            inputCurrency.select_by_value('2')
        
        inputReason.select_by_value('1')
        inputSumm.send_keys(test[1])

        continue_btns[2].click()
        time.sleep(1)

        inputName = driver.find_element(By.ID, '_credit_fio')
        inputPhone = driver.find_element(By.ID, '_credit_phone')

        inputName.send_keys(test[2])
        inputPhone.send_keys(test[3])

        continue_btns[3].click()
        time.sleep(1)

        submit = driver.find_element(By.ID, '_credit_submit')
        submit.click()

        submit_verify = driver.find_element(By.CSS_SELECTOR, 'body > div.swal2-container.swal2-center.swal2-fade.swal2-shown > div > div.swal2-actions > button.swal2-confirm.swal2-styled')
        submit_verify.click()

        time.sleep(5)
        driver.close()
        driver.quit()

def set_slider_value(driver, value):
    slider = driver.find_element(By.XPATH, '//*[@id="summ"]')
    
    slider_location = slider.location_once_scrolled_into_view
    slider_width = slider.size['width']
    slider_range = 50000 - 500
    relative_value = (value - 500) / slider_range
    pixel_offset = round(relative_value * slider_width)
    ActionChains(driver).drag_and_drop_by_offset(slider, pixel_offset, 0).perform()

def fill_ibt(test):
    url = 'https://ibt.tj/credits/kredit-na-neobkhodimye-nuzhdy/'
    driver = webdriver.Chrome()

    try:
        driver.get(url=url)
        time.sleep(2)
    except Exception as ex:
        print(ex)
    finally:
        if test[1] == 'tjs':
            inputCurrency = driver.find_element(By.ID, "tjs")
            inputCurrency.click()
        else:
            inputCurrency = driver.find_element(By.ID, "usd")
            inputCurrency.click()
        
        inputName = driver.find_element(By.ID, "name")
        inputSumm = driver.find_element(By.ID, 'summ_input')
        slider = driver.find_element(By.ID, 'summ')
        sliderval = -171

        set_slider_value(driver, 10000)

        inputName.send_keys(test[0])
        inputNumber = driver.find_element(By.ID, "number_phone")
        inputNumber.send_keys(test[1])
        inputAmount = driver.find_element(By.ID, "sum")
        inputAmount.send_keys(test[2])
        inputFile = driver.find_element(By.ID, "file-foto")
        inputFile.send_keys(test[3])

        send = driver.find_element(By.ID, 'send_loan')
        send.click()
        time.sleep(10)
        driver.close()
        driver.quit()


update()


