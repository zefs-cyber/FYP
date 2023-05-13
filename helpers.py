# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import dataframe_image as dfi
import json
import requests
import time
from bs4 import BeautifulSoup 
import urllib.parse
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
from pytesseract import pytesseract

update_date = time.time()



def find_tj(src):
    path_to_tesseract = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    path_to_image = src
    pytesseract.tesseract_cmd = path_to_tesseract

    img = Image.open(path_to_image)
    text = pytesseract.image_to_string(img, lang='rus')

    if 'точикистон' in text.lower():
        return True
    else:
        return False

def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def convert_float(num):
    if is_float(num):
        return round(float(num))

def load_json():
    with open('sessions.json', 'r') as file:
        data = json.load(file)
    return data

def save_json(data):
    with open('sessions.json', 'w') as file:
        json.dump(data, file)

def get_current_state(chat_id, session_handler):
    if chat_id in session_handler:
        return session_handler[chat_id][-1]

def set_state(chat_id, session_handler, state):
    if chat_id in session_handler:
        session_handler[chat_id][-1] = state

def get_language(chat_id, session_handler):
    if chat_id in session_handler:
        return session_handler[chat_id][1]
    
def set_language(chat_id, session_handler, language):
    if chat_id in session_handler:
        session_handler[chat_id][1] = language

def check_all(inpt, language):
    df = pd.read_excel('loan_data copy.xlsx', inpt[0], engine='openpyxl')
    if language == 'Tajik':
        banks = banks_tj
    elif language == 'Russian':
        banks = banks_ru
    else:
        banks = banks_en
    
    for i in df['Bank id']:
        df['Bank id'] = df['Bank id'].replace(i, banks[i])
    
    df.set_index('Bank id')
    if inpt[1] == 'tjs':
        selected = df.query("maxTJS >= @inpt[2] & durationTJS >= @inpt[3]")
    else:
        selected = df.query("maxUSD >= @inpt[2] & durationUSD >= @inpt[3]")

    return selected

def check(inpt, language):
    selected = check_all(inpt, language)
    return selected[selected['%'+inpt[1].upper()] == selected['%'+inpt[1].upper()].min()]

def exp_image(inpt, language):
    selected = check_all(inpt, language)
    if inpt[1] == 'tjs':
        dfi.export(selected[['Bank id', '%TJS', 'maxTJS', 'durationTJS']], 'result.png') 
    else:
        dfi.export(selected[['Bank id', '%USD', 'maxUSD', 'durationUSD']], 'result.png')

def get_links_banks(url):
  result = []
  site = requests.get(url)
  soup = BeautifulSoup(site.text, "html.parser")
  a = soup.find_all('a')

  for i in a:
    if '/files/banking_system/' in i.get('href') and 'finance_bank_pokazatel/' not in i.get('href') and i.text[0].isnumeric():
      if i.get('href') not in result:
        result.append(urllib.parse.unquote("https://www.nbt.tj" + i.get('href')))
  link = result.pop(12)
  result.insert(5, link)
  return result

def create_df(urls, names):
  url = urls[0]
  encoded_url = urllib.parse.quote(url, safe=':/')
  df = pd.read_excel(encoded_url, skiprows=3).iloc[:, 1:].dropna()

  df_all = pd.DataFrame(columns=df['INDICATORS'])
  
  for i in range(len(urls)):
    try:
      url = urls[i]
      encoded_url = urllib.parse.quote(url, safe=':/')

      if 'Tawhidbank' in urls[i]:
        df = pd.read_excel(encoded_url, skiprows=2)
      else:
        df = pd.read_excel(encoded_url, skiprows=3)

      df = df.iloc[:, 1:]  # drop first column

      if 'Arvand' not in urls[i]:
        df = df.dropna()
      else:
        df = df.drop(index=17)
        df = df.drop(index=18)

      if 'Tawhidbank' in urls[i]:
        vals = list(df[df.columns[-1]])
        vals.insert(-6, 0)
      else:
        vals = list(df[df.columns[-1]])
      df_all.loc[names[i]] = vals

    except Exception as e:
      pass
  
  return df_all

def performance(df):
  df['АSSETS'] = MinMaxScaler().fit_transform(np.array(df['АSSETS']).reshape(-1,1))
  df['LIABILITIES'] = MinMaxScaler().fit_transform(np.array(df['LIABILITIES']).reshape(-1,1))
  df['BALANCE СAPITAL'] = MinMaxScaler().fit_transform(np.array(df['BALANCE СAPITAL']).reshape(-1,1))

  # Set weights
  w1 = 0.2
  w2 = 0.15
  w3 = 0.15
  w4 = 0.1
  w5 = 0.1
  w6 = 0.1
  w7 = 0.1
  w8 = 0.05
  w9 = 0.05

  # Calculate performance score
  df['Performance'] = w1 * df['АSSETS'] + \
                      w2 * df['LIABILITIES'] + \
                      w3 * df['BALANCE СAPITAL'] + \
                      w4 * df['Return on assets (ROA, %)'] + \
                      w5 * df['Return on equity (ROE, %)'] + \
                      w6 * df['Liquidity Ratios (К2.1, %)'] + \
                      w7 * df['Number of branches'] + \
                      w8 * df['Number of banking service centers '] + \
                      w9 * df['Number of ATMs']
  df['Rank'] = df['Performance'].rank(method='dense', ascending=False)

  return df

banks_en = [
    'Orienbank',                         #0+
    'Amonatbank',                        #1+
    'Eskhata Bank',                      #2+
    'Tawhidbank',                        #3NoData
    'The First MicroFinanceBank',        #4Data presented in pdf
    'Bonki Rushdi Tojikiston',           #5+
    '"Tjiorat" Bank Branch',             #6??
    'Halyk Bank of Tajikistan',          #7NoCredit
    'Bank "Arvand"',                     #8+
    'Spitamen Bank',                     #9+ 
    'International Bank of Tajikistan',  #10+
    'Commerce Bank of Tajikistan',       #11+
    'Alif Bank',                         #12No loans
    'Sanoatsodirotbonk',                 #13+
    'Dushanbe City Bank'                 #14No loans
]

websites = [
    'https://orienbank.tj/individuals/loans/consumer',
    'https://www.amonatbonk.tj/ru/personal/loans/potrebitelskiy-kredit/',
    'https://eskhata.com/individuals/lending/lending_types/',
    'https://tawhidbank.tj/',
    'https://fmfb.tj/ru/consumer-loans/',
    'https://brt.tj/ru/porteb',
    'http://tejaratbank.tj/ru/individuals/credits_individuals/',
    'https://halykbank.tj/',
    'https://www.arvand.tj/cl/kredity/potrebitelskiy',
    'https://www.spitamenbank.tj/ru/products/personal/credit/potrebitelskie-kredity/',
    'https://ibt.tj/credits/kredit-na-neobkhodimye-nuzhdy/',
    'https://cbt.tj/retail/credits/barakat',
    'https://pul.alif.tj/',
    'https://ssb.tj/en/about?type=4',
    'https://credit.dc.tj/'
]

columns_en = [
    'RateTJS',
    'AmountTJS',
    'PeriodTJS',
    'RateUSD',
    'AmountUSD',
    'PeriodUSD',
]

banks_tj = [
    'Ориенбонк',
    'Амонатбонк',
    'Бонки Эсхата',
    'Тавхидбонк',
    'Аввалин бонки молиявии хурд',
    'Бонки рушди Точикистон',
    'Бонки Тичорат',
    'Халик бонк Точикистон',
    'Бонки Арванд',
    'Спитамен бонк',
    'Бонки байналмилалии Точикистон',
    'Коммерсбонки Точикистон',
    'Алиф бонк',
    'Саноатсодиротбонк',
    'Душанбе сити бонк']

columns_tj = [
    'ФоизTJS',
    'КредитTJS',
    'МухлатTJS',
    'ФоизUSD',
    'КредитUSD',
    'МухлатUSD',
]

banks_ru = [
    'Ориёнбанк',
    'Амонатбанк',
    'Банк Эсхата',
    'Тавхидбанк',
    'Первый микрофинансовый Банк',
    'Бонки рушди Точикистон',
    'Филиал банка "Тиджорат"',
    'Халык Банк Таджикистана',
    'Банк Арванд',
    'Спитамен Банк',
    'Международный банк Таджикистана',
    'Коммерцбанк Таджикистана',
    'Алиф Банк',
    'Саноатсодиротбанк',
    'Душанбе Сити Банк'
]

columns_ru = [
    'СтавкаTJS',
    'МаксСуммаTJS',
    'ПериодTJS',
    'СтавкаUSD',
    'МаксСуммаUSD',
    'ПериодdUSD',
]

currencies = ['USD', 'EUR', 'CNY', 'CHF', 'RUB', 
              'UZS', 'KGS', 'KZT', 'BYN', 'IRR', 
              'AFN', 'PKR', 'TRY', 'TMT', 'GBP', 
              'AUD', 'DKK', 'ISK', 'CAD', 'KWD', 
              'NOK', 'SGD', 'SEK', 'JPY', 'AZN', 
              'AMD', 'GEL', 'MDL', 'UAH', 'AED', 
              'SAR', 'INR', 'PLN', 'MYR', 'THB']

link_nbt = 'https://www.nbt.tj/en/banking_system/finance_bank_pokazatel.php'



