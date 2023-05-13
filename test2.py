# -*- coding: cp1251 -*-

import pandas as pd
import dataframe_image as dfi

test_l = ["consumer loan", 'tjs', 270000, 6]
test_e = ['rub', 'usd', 100000]

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
        selected = df.query("maxTJS >= @inpt[3] & durationTJS >= @inpt[3]")
    else:
        selected = df.query("maxUSD >= @inpt[3] & durationUSD >= @inpt[3]")
    return selected

def check(inpt, language):
    selected = check_all(inpt, language)
    return selected[selected['%'+inpt[1].upper()] == selected['%'+inpt[1].upper()].min()]

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


session_handler = load_json()

language = 'Tajik'
user_id = 'dilovar123'
chat_id = 'dilovarchat3'
username = 'dilovar'
state1 = 'Start'
state2 = 'Language'


session_handler[chat_id] = [language, username, test_e, test_l, state1] 


set_state(chat_id, session_handler, state2)

print(get_current_state(chat_id, session_handler))

save_json(session_handler)


# {600: -171, 700: -170, 800: -169, 1000: -167, 1300: -166, 1400: -165, 1500: -164, 1700: -163, 1800: -162, 2000: -161, 2100: -160, 2300: -159, 2400: -158, 2600: -157, 2700: -156, 2800: -155, 3000: -154, 3100: -153, 3300: -152, 3400: -151, 3600: -150, 3700: -149, 3900: -148, 4000: -147, 4100: -146, 4300: -145, 4400: -144, 4600: -143, 4700: -142, 4900: -141, 5000: -140, 5200: -139, 5300: -138, 5400: -137, 5600: -136, 5700: -135, 5900: -134, 6000: -133, 6200: -132, 6300: -131, 6500: -130, 6600: -129, 6800: -128, 6900: -127, 7000: -126, 7200: -125, 7300: -124, 7500: -123, 7600: -122, 7800: -121, 7900: -120, 8100: -119, 8200: -118, 8300: -117, 8500: -116, 8600: -115, 8800: -114, 8900: -113, 9100: -112, 9200: -111, 9400: -110, 9500: -109, 9600: -108, 9800: -107, 9900: -106, 10100: -105, 10200: -104, 10400: -103, 10500: -102, 10700: -101, 10800: -100, 10900: -99, 11100: -98, 11200: -97, 11400: -96, 11500: -95, 11700: -94, 11800: -93, 12000: -92, 12100: -91, 12300: -90, 12400: -89, 12500: -88, 12700: -87, 12800: -86, 13000: -85, 13100: -84, 13300: -83, 13400: -82, 13600: -81, 13700: -80, 13800: -79, 14000: -78, 14100: -77, 14300: -76, 14400: -75, 14600: -74, 14700: -73, 14900: -72, 15000: -71, 15100: -70, 15300: -69, 15400: -68, 15600: -67, 15700: -66, 15900: -65, 16000: -64, 16200: -63, 16300: -62, 16400: -61, 16600: -60, 16700: -59, 16900: -58, 17000: -57, 17200: -56, 17300: -55, 17500: -54, 17600: -53, 17800: -52, 17900: -51, 18000: -50, 18200: -49, 18300: -48, 18500: -47, 18600: -46, 18800: -45, 18900: -44, 19100: -43, 19200: -42, 19300: -41, 19500: -40, 19600: -39, 19800: -38, 19900: -37, 20100: -36, 20200: -35, 20400: -34, 20500: -33, 20600: -32, 20800: -31, 20900: -30, 21100: -29, 21200: -28, 21400: -27, 21500: -26, 21700: -25, 21800: -24, 21900: -23, 22100: -22, 22200: -21, 22400: -20, 22500: -19, 22700: -18, 22800: -8, 23000: -16, 23100: -15, 23300: -14, 23400: -6, 23500: -12, 23700: -11, 23800: -10, 24000: -4, 24300: -7, 24600: -5, 23600: -3, 25000: 1, 24900: 0, 25300: 2, 25700: 3, 26300: 4, 27000: 12, 26100: 6, 27100: 7, 26400: 8, 27700: 17, 26700: 10, 28300: 21, 27200: 13, 27300: 14, 27400: 15, 27600: 16, 27900: 18, 28000: 19, 28200: 20, 28500: 22, 28600: 23, 28800: 24, 28900: 25, 29000: 26, 29200: 27, 29300: 28, 29500: 29, 29600: 30, 29800: 31, 29900: 32, 30100: 33, 30200: 34, 30300: 35, 30500: 36, 30600: 37, 30800: 38, 30900: 39, 31100: 40, 31200: 41, 31400: 42, 31500: 43, 31600: 44, 31800: 45, 31900: 46, 32100: 47, 32200: 48, 32400: 49, 32500: 50, 32700: 51, 32800: 52, 32900: 53, 33100: 54, 33200: 55, 33400: 56, 33500: 57, 33700: 58, 33800: 59, 34000: 60, 34100: 61, 34300: 62, 34400: 63, 34500: 64, 34700: 65, 34800: 66, 35000: 67, 35100: 68, 35300: 69, 35400: 70, 35600: 71, 35700: 72, 35800: 73, 36000: 74, 36100: 75, 36300: 76, 36400: 77, 36600: 78, 36700: 79, 36900: 80, 37000: 81, 37100: 82, 37300: 83, 37400: 84, 37600: 85, 37700: 86, 37900: 87, 38000: 88, 38200: 89, 38300: 90, 38400: 91, 38600: 92, 38700: 93, 38900: 94, 39000: 95, 39200: 96, 39300: 97, 39500: 98, 39600: 99, 39800: 100, 39900: 101, 40000: 102, 40200: 103, 40300: 104, 40500: 105, 40600: 106, 40800: 107, 40900: 108, 41100: 109, 41200: 110, 41300: 111, 41500: 112, 41600: 113, 41800: 114, 41900: 115, 42100: 116, 42200: 117, 42400: 118, 42500: 119, 42600: 120, 42800: 121, 42900: 122, 43100: 123, 43200: 124, 43400: 125, 43500: 126, 43700: 127, 43800: 128, 43900: 129, 44100: 130, 44200: 131, 44400: 132, 44500: 133, 44700: 134, 44800: 135, 45000: 136, 45100: 137, 45300: 138, 45400: 139, 45500: 140, 45700: 141, 45800: 142, 46000: 143, 46100: 144, 46300: 145, 46400: 146, 46600: 147, 46700: 148, 46800: 149, 47000: 150, 47100: 151, 47300: 152, 47400: 153, 47600: 154, 47700: 155, 47900: 156, 48000: 157, 48100: 158, 48300: 159, 48400: 160, 48600: 161, 48700: 162, 48900: 163, 49000: 164, 49200: 165, 49300: 166, 49400: 167, 49600: 168, 49700: 169, 49900: 170}
