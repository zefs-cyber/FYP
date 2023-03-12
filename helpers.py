# -*- coding: cp1251 -*-

import pandas as pd
import dataframe_image as dfi


def check_all(inpt, language):
    df = pd.read_excel('loan_data.xlsx', inpt[0], engine='openpyxl')
    if language == 'Tajik':
        for i in df['Bank id']:
            df['Bank id'] = df['Bank id'].replace(i, banks_tj[i])
    elif language == 'Russian':
        for i in df['Bank id']:
            df['Bank id'] = df['Bank id'].replace(i, banks_ru[i])
    else:
        for i in df['Bank id']:
            df['Bank id'] = df['Bank id'].replace(i, banks_en[i])
    df.set_index('Bank id')
    if inpt[2] == 'tjs':
        selected = df.query("maxTJS >= @inpt[1] & durationTJS >= @inpt[3]")
    else:
        selected = df.query("maxUSD >= @inpt[1] & durationUSD >= @inpt[3]")
    return selected

def check(inpt, language):
    selected = check_all(inpt, language)
    return selected[selected['%'+inpt[2].upper()] == selected['%'+inpt[2].upper()].min()]

def exp_image(inpt, language):
    selected = check_all(inpt, language)
    if inpt[2] == 'tjs':
        dfi.export(selected[['Bank id', '%TJS', 'maxTJS', 'durationTJS']], 'result.png') 
    else:
        dfi.export(selected[['Bank id', '%USD', 'maxUSD', 'durationUSD']], 'result.png')

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