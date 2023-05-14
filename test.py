# from pytesseract import pytesseract
# from PIL import Image 
# import re


# path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# names = ['Ibrohim', 'Umidbek', 'Milena']

# def find_name(pic, name):
#     pytesseract.tesseract_cmd = path_to_tesseract
#     text = pytesseract.image_to_string(pic)
#     result = re.sub(r'[^\x00-\x7f]',r'', text)
#     if name.upper() in result:
#         return True
#     else:
#         return False




# for name in names:
#     for i in range(1,4):
#         img = Image.open(f'C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\img{i}.jpg')
#         print(find_name(img, name))




# import cv2
# template = cv2.imread("C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\icon.jpg", cv2.IMREAD_GRAYSCALE)
# for i in range(1,4):
#     image = cv2.imread(f"C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\img{i}.jpg", cv2.IMREAD_GRAYSCALE)
#     result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     threshold = 0.8
#     print(max_val)
#     if max_val > threshold:
#         print("Icon is present in the image")
#     else:
#         print("Icon is not present in the image")


import requests
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# test = ['Mashrabov Dilovar Khamidulloevich', 556550088, 10000, 'C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\img1.jpg']
# test = [0,'tjs',50000]

test = ['tjs', 10000, 'AAAA', '+992555555555']

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

def fill_amonatbank(test):
    url = 'https://www.amonatbonk.tj/en/personal/loans/potrebitelskiy-kredit/#formCredit'
    driver = webdriver.Chrome()

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
    driver = webdriver.Chrome()

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
        
        inputSumm = driver.find_element(By.ID, 'summ_input')
        slider = driver.find_element(By.ID, 'summ')
        sliderval = -171

        set_slider_value(driver, 10000)

        # Calculate the position of the slider for the given value
        # position = int((test[2] - slider_min) / (slider_max - slider_min) * 100)

        # print(position)

        # action.move_to_element(slider).click_and_hold().move_by_offset(position, 0).release().perform()

        # inputName.send_keys(test[0])
        # inputNumber = driver.find_element(By.ID, "number_phone")
        # inputNumber.send_keys(test[1])
        # inputAmount = driver.find_element(By.ID, "sum")
        # inputAmount.send_keys(test[2])
        # inputFile = driver.find_element(By.ID, "file-foto")
        # inputFile.send_keys(test[3])

        # send = driver.find_element(By.ID, 'send_loan')
        # send.click()
        time.sleep(10)
        driver.close()
        driver.quit()


