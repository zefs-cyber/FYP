# -*- coding: cp1251 -*-

import pandas as pd
import dataframe_image as dfi

test = ["consumer loan", 270000, 'tjs', 6]


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

banks_en = [
    'Orienbank',
    'Amonatbank',
    'Eskhata Bank',
    'Tawhidbank',
    'The First MicroFinanceBank',
    'Bonki Rushdi Tojikiston',
    '"Tjiorat" Bank Branch',
    'Halyk Bank of Tajikistan',
    'Bank "Arvand"',
    'Spitamen Bank',
    'International Bank of Tajikistan',
    'Commerce Bank of Tajikistan',
    'Alif Bank',
    'Sanoatsodirotbonk',
    'Dushanbe City Bank'
]

columns_en = [
    'RateTJS',
    'AmountTJS',
    'PeriodTJS',
    'RateUSD',
    'AmountUSD',
    'PeriodUSD',
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

columns_en = [
    'СтавкаTJS',
    'МаксСуммаTJS',
    'ПериодTJS',
    'СтавкаUSD',
    'МаксСуммаUSD',
    'ПериодdUSD',
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



# print(check(test, 'English'))
# exp_image(test, 'English')
# print(check(test, "English")['Bank id'].values[0])
# print(websites[banks_en.index(check(test, "English")['Bank id'].values[0])])

import json

with open('sessions.json', 'r') as file:
    session_handler = json.load(file)

user_id = 'dilovar123'
chat_id = 'dilovarchat1'
username = 'dilovar'

if chat_id not in session_handler:
    session_handler[chat_id] = [user_id, username, [], []] 


print(session_handler)

with open('sessions.json', 'w') as file:
    json.dump(session_handler, file)

