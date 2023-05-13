# -*- coding: utf-8 -*-

import requests
import re

def exchange_rates():
      """return dictionary with exchange rates"""

      url = 'https://nbt.tj/tj/kurs/rss.php'
      rss = requests.get(url).text

      names_tj = ['Доллари ИМА', 'ЕВРО', 'Юани Чин', 'Франки Швейтсария', 
                  'Рубли Русия', 'Сӯми Ӯзбекистон', 'Соми Қирғизистон', 
                  'Тангаи Қазоқистон', 'Рубли нави Белорус', 'Риёли Эрон', 
                  'Афғонии  Афғонистон', 'Рупияи Покистон', 'Лири Туркия', 
                  'Манати нави Туркманистон', 'Фунти стерлингҳои Инглистон', 
                  'Доллари Австралия', 'Кронаи Дания', 'Кронаи Исландия', 
                  'Доллари Канада', 'Динори Қувайт', 'Кронаи Норвегия', 
                  'Доллари Сингапур', 'Кронаи Шветсия', 'Йени Ҷопон', 
                  'Манати Озарбойҷон', 'Драми Арманистон', 'Ларии Гурҷистон', 
                  'Лейи Молдова', 'Гривнаи Украина', 'Дирхами АМА', 
                  'Риёли Арабистони Саудӣ', 'Рупияи Ҳиндустон', 'Злотийи Лаҳистон', 
                  'Ринггити Малайзия', 'Бати Таиланд']
      names_other = ['USD', 'EUR', 'CNY', 'CHF', 'RUB', 
                  'UZS', 'KGS', 'KZT', 'BYN', 'IRR', 
                  'AFN', 'PKR', 'TRY', 'TMT', 'GBP', 
                  'AUD', 'DKK', 'ISK', 'CAD', 'KWD', 
                  'NOK', 'SGD', 'SEK', 'JPY', 'AZN', 
                  'AMD', 'GEL', 'MDL', 'UAH', 'AED', 
                  'SAR', 'INR', 'PLN', 'MYR', 'THB']

      ex = {"CURRENCY CODE": [],
            "UNIT" : [],
            "RATE" : [],
            "NAMES_TJ" : names_tj,
            "NAMES_OTHER" : names_other}

      start = [i.start() for i in re.finditer('<title>', rss)]
      end = [i.start() for i in re.finditer('</title>', rss)]
      titles = [rss[start[i]+7:end[i]][rss[start[i]+7:end[i]].find("|")+1:] for i in range(1,len(start))]

      for i in titles:
            code = i[i.find("CURRENCY CODE: ")+len('CURRENCY CODE: '):i.find("| UNIT")]
            unit = i[i.find("UNIT: ")+len('UNIT: '):i.find("| RATE")]
            rate = i[i.find("RATE: ")+len('RATE: '):]
            ex["CURRENCY CODE"].append(code)
            ex["UNIT"].append(unit)
            ex["RATE"].append(rate)
      
      return ex