# -*- coding: utf-8 -*-

import telebot
import time
from telebot import types
from datetime import datetime
import config
import dbworker
import auth
import exchange_rates_rss
import parsers
from helpers import *
import os


TOKEN = auth.TOKEN

session_handler = load_json()

ex = exchange_rates_rss.exchange_rates()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    global session_handler

    welcome_msg = f"Привет {message.from_user.first_name}!\nКакой язык вы предпочитаете?"

    if message.chat.id not in session_handler:
        session_handler[message.chat.id] = [message.from_user.first_name, "", [], [], [], config.States.START.value]
    else:
        session_handler[message.chat.id] = [message.from_user.first_name, "", [], [], [], config.States.START.value]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🇹🇯 Tajik")
    item2 = types.KeyboardButton("🇷🇺 Russian")
    item3 = types.KeyboardButton("🇬🇧 English")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    if time.time() - update_date > 24*60*60:
        df = parsers.update()
        df.to_excel('loan_data copy.xlsx')

    bot.send_message(message.chat.id, welcome_msg, parse_mode = "html", reply_markup=markup)
    set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.LANGUAGE.value)
def get_language_handler(message):
    global session_handler
    if message.text[3:] == "Tajik":
        set_language(message.chat.id, session_handler, message.text[3:])
        
        #Keyboard inline - tajik
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кӯмак бо қарз")
        item2 = types.KeyboardButton("Мубодилаи асъор")
        item3 = types.KeyboardButton("Ариза ба қарз")
        item4 = types.KeyboardButton('Кӯмак')
        item5 = types.KeyboardButton("Бозгашт")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)

        bot.send_message(message.chat.id, "Ман ба кор таёрам!\nМан чӣ тавр ба шумо кӯмак расонам?", parse_mode="html", reply_markup=markup)
        set_state(message.chat.id, session_handler, config.States.ACTION.value)
    
    elif message.text[3:] == "Russian":
        set_language(message.chat.id, session_handler, message.text[3:])
        
        #Keyboard inline - russian
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Помощь с кредитом")
        item2 = types.KeyboardButton("Курс валют")
        item3 = types.KeyboardButton("Подать заявку на кредит")
        item4 = types.KeyboardButton("Помощь")
        item5 = types.KeyboardButton("Назад")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)

        bot.send_message(message.chat.id, "Я готов к работе!\nЧем могу я вам помочь?", parse_mode="html", reply_markup=markup)
        set_state(message.chat.id, session_handler, config.States.ACTION.value)
    
    elif message.text[3:] == "English":
        set_language(message.chat.id, session_handler, message.text[3:])

        #Keyboard inline - english
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Help with a loan")
        item2 = types.KeyboardButton("Exchange Rates")
        item3 = types.KeyboardButton("Apply for loan")
        item4 = types.KeyboardButton("Help")
        item5 = types.KeyboardButton("Back")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)

        bot.send_message(message.chat.id, "I am ready to work!\nHow can i help you", parse_mode="html", reply_markup=markup)
        set_state(message.chat.id, session_handler, config.States.ACTION.value)
    else:
        if message.text[3:] == "Tajik":
            bot.send_message(message.chat.id, "Ман нафаҳмидам, ки шумо чӣ дар назар доред!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)
        elif message.text[3:] == "Russian":
            bot.send_message(message.chat.id, "Я не понял, что вы имеету в виду!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)
        elif message.text[3:] == "English":
            bot.send_message(message.chat.id, "I don't know what you mean!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)
        else:
            bot.send_message(message.chat.id, "I don't know what you mean!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)
    
@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.ACTION.value)
def get_start(message):
    """Action State"""
    global session_handler

    if get_language(message.chat.id, session_handler) == "Tajik":
        if message.text == "Кӯмак бо қарз":           
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Қарзи истеъмолӣ")
            item2 = types.KeyboardButton("Қарзи мошин")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Бо кадом мақсад шумо мехоҳед қарз гиред?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_PURPOSE.value)
    
        elif message.text == "Мубодилаи асъор":
            bot.send_message(message.chat.id, "Кадом асъорро иваз кардан мехоҳед?\nМасалан: USD, RUB, KGS", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_FROM.value)
        
        elif message.text =='Ариза ба қарз':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Амонатбонк")
            item2 = types.KeyboardButton("Коммерс Бонки Точикистон")
            item3 = types.KeyboardButton("Бозгашт")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Лутфан бонкро интихоб кунед", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_SELECT.value)

        elif message.text == "Бозгашт":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🇹🇯 Tajik")
            item2 = types.KeyboardButton("🇷🇺 Russian")
            item3 = types.KeyboardButton("🇬🇧 English")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Шумо ба кадом забон бартарӣ медиҳед?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)
        
        elif message.text == "Кӯмак":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Кӯмак бо қарз")
            item2 = types.KeyboardButton("Мубодилаи асъор")
            item3 = types.KeyboardButton("Ариза ба қарз")
            item4 = types.KeyboardButton('Кӯмак')
            item5 = types.KeyboardButton("Бозгашт")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)
            markup.add(item5)

            bot.send_message(message.chat.id, "Ин аст дастури корбар барои бот ва чӣ тавр истифода бурдани он", parse_mode="html")
            bot.send_message(message.chat.id, "https://zefs-cyber.github.io/loansInTajikistan.github.io/", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)

        else:
            bot.send_message(message.chat.id, "Ман шуморо намефаҳмам, лутфан такрор кунед!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.ACTION.value)
            

    elif get_language(message.chat.id, session_handler) == "Russian":
        if message.text == "Помощь с кредитом":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Потребительский кредит")
            item2 = types.KeyboardButton("Автокредит")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "C какой целью вы хотите взять в кредит?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_PURPOSE.value)

        elif message.text == "Курс валют":
            bot.send_message(message.chat.id, "Какую валюту вы хотите поменять?\nНапример: USD, RUB, KGS", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_FROM.value)

        elif message.text =='Подать заявку на кредит':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Амонатбанк")
            item2 = types.KeyboardButton("Комерческий Банк Таджикистана")
            item3 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Пожалуйста выберите банк", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_SELECT.value)
        
        elif message.text == "Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🇹🇯 Tajik")
            item2 = types.KeyboardButton("🇷🇺 Russian")
            item3 = types.KeyboardButton("🇬🇧 English")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Какой язык вы предпочитаете?", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)
        
        elif message.text == "Помощь":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Помощь с кредитом")
            item2 = types.KeyboardButton("Курс валют")
            item3 = types.KeyboardButton("Подать заявку на кредит")
            item4 = types.KeyboardButton("Помощь")
            item5 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)
            markup.add(item5)

            bot.send_message(message.chat.id, "Вот руководство пользователя для бота и как его использовать", parse_mode="html")
            bot.send_message(message.chat.id, "https://zefs-cyber.github.io/loansInTajikistan.github.io/", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)
        else:
            bot.send_message(message.chat.id, "Я вас не понимаю, пожалуйста повторите!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.ACTION.value)
    
    elif get_language(message.chat.id, session_handler) == "English":
        if message.text == "Help with a loan":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Consumer Loan")
            item2 = types.KeyboardButton("Car Loan")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "For what purpose do you want to get loan?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_PURPOSE.value)

        elif message.text == "Exchange Rates":
            bot.send_message(message.chat.id, "What currency do you want to change?\nFor example: USD, RUB, KGS", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_FROM.value)
        
        elif message.text == 'Apply for loan':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Amonatbank")
            item2 = types.KeyboardButton("Commerce Bank Tajikistan")
            item3 = types.KeyboardButton("Back")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Please select bank", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_SELECT.value)

        elif message.text == "Back":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🇹🇯 Tajik")
            item2 = types.KeyboardButton("🇷🇺 Russian")
            item3 = types.KeyboardButton("🇬🇧 English")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "What language do you prefer?", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LANGUAGE.value)

        elif message.text == "Help":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Help with a loan")
            item2 = types.KeyboardButton("Exchange Rates")
            item3 = types.KeyboardButton("Apply for loan")
            item4 = types.KeyboardButton("Help")
            item5 = types.KeyboardButton("Back")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)
            markup.add(item5)

            bot.send_message(message.chat.id, "Here is the user manual for the bot and how to use it", parse_mode="html")
            bot.send_message(message.chat.id, "https://zefs-cyber.github.io/loansInTajikistan.github.io/", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)

        else:
            bot.send_message(message.chat.id, "I don't understand you, please repeat!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.ACTION.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.CURRENCY_FROM.value)
def get_currency_from(message):
    global session_handler
    if message.text.upper() in ex['NAMES_OTHER']:
        
        if len(session_handler[message.chat.id][2]) < 3:
            session_handler[message.chat.id][2].append(message.text.upper())
        else:
            session_handler[message.chat.id][2][0] = message.text.upper()

        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Шумо ба кадом асъор иваз кардан мехоҳед?\nМасалан: USD, RUB, KGS", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_TO.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "На какую валюту вы хотите поменять?\nНапример: USD, RUB, KGS", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_TO.value)

        else:
            bot.send_message(message.chat.id, "To what currency do you want to change?\nFor example: USD, RUB, KGS", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_TO.value)

    else:        
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан асъори дурустро ворид кунед!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_FROM.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите правильную валюту!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_FROM.value)

        else:
            bot.send_message(message.chat.id, "Please enter the correct currency!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_FROM.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.CURRENCY_TO.value)
def get_currency_to(message):
    global session_handler

    if message.text.upper() in ex['NAMES_OTHER']:
        if len(session_handler[message.chat.id][2]) < 3:
            session_handler[message.chat.id][2].append(message.text.upper())
        else:
            session_handler[message.chat.id][2][1] = message.text.upper()

        currency_from = session_handler[message.chat.id][2][0]

        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, f"Шумо чанд {currency_from} мехоҳед иваз кунед?", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_AMOUNT.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, f"Сколько {currency_from} вы хотите поменять?", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_AMOUNT.value)

        else:
            bot.send_message(message.chat.id, f"How many {currency_from} do you want to change?", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_AMOUNT.value)

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан асъори дурустро ворид кунед!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_TO.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите правильную валюту!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_TO.value)

        else:
            bot.send_message(message.chat.id, "Please enter the correct currency!", parse_mode="html")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_TO.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.CURRENCY_AMOUNT.value)
def get_currency_amount(message):
    global session_handler

    if message.text.isnumeric():
        if len(session_handler[message.chat.id][2]) < 3:
            session_handler[message.chat.id][2].append(int(message.text))
        else:
            session_handler[message.chat.id][2][2] = int(message.text)

        print(session_handler[message.chat.id][2])
        amount = session_handler[message.chat.id][2][2]
        currency_from = session_handler[message.chat.id][2][0]
        currency_to = session_handler[message.chat.id][2][1]

        i1 = ex['NAMES_OTHER'].index(currency_from)
        i2 = ex['NAMES_OTHER'].index(currency_to)
        val = amount * (float(ex['UNIT'][i2]) / float(ex['RATE'][i2])) / (float(ex['UNIT'][i1]) / float(ex['RATE'][i1]))
        
        amount = session_handler[message.chat.id][2][2]
        currency_from = session_handler[message.chat.id][2][0]
        currency_to = session_handler[message.chat.id][2][1]

        if get_language(message.chat.id, session_handler) == 'Tajik':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Кӯмак бо қарз")
            item2 = types.KeyboardButton("Мубодилаи асъор")
            item3 = types.KeyboardButton("Ариза ба қарз")
            item4 = types.KeyboardButton("Бозгашт")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)

            bot.send_message(message.chat.id, f"Бо {amount}{currency_from} шумо {round(val, 2)}{currency_to} мегиред", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Помощь с кредитом")
            item2 = types.KeyboardButton("Курс валют")
            item3 = types.KeyboardButton("Подать заявку на кредит")
            item4 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)

            bot.send_message(message.chat.id, f"За {amount}{currency_from} вы получите {round(val, 2)}{currency_to}", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Help with a loan")
            item2 = types.KeyboardButton("Exchange Rates")
            item3 = types.KeyboardButton("Apply for loan")
            item4 = types.KeyboardButton("Back")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)

            bot.send_message(message.chat.id, f"For {amount}{currency_from} you will get {round(val, 2)}{currency_to}", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)
        save_json(session_handler)

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_AMOUNT.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_AMOUNT.value)

        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            set_state(message.chat.id, session_handler, config.States.CURRENCY_AMOUNT.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.LOAN_PURPOSE.value)
def get_loan_purpose(message):
    global session_handler

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('TJS')
    item2 = types.KeyboardButton('USD')
    markup.add(item1)
    markup.add(item2)

    if get_language(message.chat.id, session_handler) == 'Tajik':

        if message.text == "Қарзи истеъмолӣ" or message.text == "Қарзи мошин":

            if message.text == "Қарзи истеъмолӣ":
                if len(session_handler[message.chat.id][3]) < 4:
                    session_handler[message.chat.id][3].append('consumer loan')
                else:
                    session_handler[message.chat.id][3][0] = ('consumer loan')

            else:
                if len(session_handler[message.chat.id][3]) < 4:
                    session_handler[message.chat.id][3].append('car loan')
                else:
                    session_handler[message.chat.id][3][0] = ('car loan')

            bot.send_message(message.chat.id, "Шумо бо кадом асъор қарз гирифтан мехоҳед?",  reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_CURRENCY.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Қарзи истеъмолӣ")
            item2 = types.KeyboardButton("Қарзи мошин")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Бо кадом мақсад шумо мехоҳед қарз гиред?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_PURPOSE.value)

    elif get_language(message.chat.id, session_handler) == 'Russian':

        if message.text == 'Потребительский кредит' or message.text == 'Автокредит':

            if message.text == "Потребительский кредит":
                if len(session_handler[message.chat.id][3]) < 4:
                    session_handler[message.chat.id][3].append('consumer loan')
                else:
                    session_handler[message.chat.id][3][0] = ('consumer loan')
                
            else:
                if len(session_handler[message.chat.id][3]) < 4:
                    session_handler[message.chat.id][3].append('car loan')
                else:
                    session_handler[message.chat.id][3][0] = ('car loan')

            bot.send_message(message.chat.id, "В какой валюте вы хотите взять кредит?", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_CURRENCY.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Потребительский кредит")
            item2 = types.KeyboardButton("Автокредит")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "C какой целью вы хотите взять в кредит?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_PURPOSE.value)

    else:
        if message.text == 'Consumer Loan' or message.text == 'Car Loan':
            
            if message.text == "Consumer Loan":
                if len(session_handler[message.chat.id][3]) < 4:
                    session_handler[message.chat.id][3].append('consumer loan')
                else:
                    session_handler[message.chat.id][3][0] = ('consumer loan')

            else:
                if len(session_handler[message.chat.id][3]) < 4:
                    session_handler[message.chat.id][3].append('car loan')
                else:
                    session_handler[message.chat.id][3][0] = ('car loan')

            bot.send_message(message.chat.id, "In what currency do you want to take a loan?", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_CURRENCY.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Consumer Loan")
            item2 = types.KeyboardButton("Car Loan")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "For what purpose do you want to get loan?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_PURPOSE.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.LOAN_CURRENCY.value)
def get_loan_currency(message):
    global session_handler

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('TJS')
    item2 = types.KeyboardButton('USD')
    markup.add(item1)
    markup.add(item2)
    
    if message.text == "TJS" or message.text == "USD":
        if len(session_handler[message.chat.id][3]) < 4:
            session_handler[message.chat.id][3].append(message.text.lower())
        else:
            session_handler[message.chat.id][3][1] = message.text.lower()

        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Шумо чӣ қадар қарз гирифтан мехоҳед?")
            set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Сколько вы хотите взять в кредит?")
            set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)

        else:
            bot.send_message(message.chat.id, "How much do you want to borrow?")
            set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан яке аз вариантҳоро интихоб кунед!", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_CURRENCY.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста выберите один из вариантов!", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_CURRENCY.value)

        else:
            bot.send_message(message.chat.id, "Please select one of the options!", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.LOAN_CURRENCY.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.LOAN_AMOUNT.value)
def get_loan_amount(message):
    if (message.text.isnumeric() or is_float(message.text)):
        if convert_float(message.text) <= 0:
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Лутфан рақами аз сифр калонтарро ворид кунед")
                set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)

            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "Пожалуйста введите цифру больше нуля")
                set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)

            else:
                bot.send_message(message.chat.id, "Please enter a number greater than zero")
                set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)
        else:

            if len(session_handler[message.chat.id][3]) < 4:
                session_handler[message.chat.id][3].append(convert_float(message.text))
            else:
                session_handler[message.chat.id][3][2] = convert_float(message.text)

            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Шумо ба кадом Мӯҳлат қарз гирифтан мехоҳед?\n(Лутфан, давраро бо моҳҳо ворид кунед)")
                set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "На какой срок вы хотите взять кредит?\n(Пожалуйста введите срок в месяцах)")
                set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

            else:
                bot.send_message(message.chat.id, "For how long do you want to take out a loan?\n(Please enter the period in months)")
                set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)
        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            set_state(message.chat.id, session_handler, config.States.LOAN_AMOUNT.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.LOAN_DURATION.value)
def get_loan_duration(message):
    global session_handler
    
    if (message.text.isnumeric() or is_float(message.text)):
        if convert_float(message.text) <= 0:
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Лутфан рақами аз сифр калонтарро ворид кунед")
                set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "Пожалуйста введите цифру больше нуля")
                set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

            else:
                bot.send_message(message.chat.id, "Please enter a number greater than zero")
                set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)
        else:

            if len(session_handler[message.chat.id][3]) < 4:
                session_handler[message.chat.id][3].append(convert_float(message.text))
            else:
                session_handler[message.chat.id][3][3] = convert_float(message.text)

            loan_user = session_handler[message.chat.id][3]
            language = get_language(message.chat.id, session_handler)
            exp_image(loan_user, language)

            print(f'{message.from_user.first_name} - image exported; {str(session_handler[message.chat.id])}; {language}')


            if len(check(loan_user, language)) > 0:
                if language == 'Tajik':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Кӯмак бо қарз")
                    item2 = types.KeyboardButton("Мубодилаи асъор")
                    item3 = types.KeyboardButton("Ариза ба қарз")
                    item4 = types.KeyboardButton("Бозгашт")
                    markup.add(item1)
                    markup.add(item2)
                    markup.add(item3)
                    markup.add(item4)
                    bot.send_message(message.chat.id, "Натиҷаҳои барои талаботи шумо:", reply_markup=markup)
                    bot.send_photo(message.chat.id, open('result.png', 'rb'))
                    bot.send_message(message.chat.id, check(loan_user, language)['Bank id'].values[0] + ' фоизи пасттаринро барои қарзе, ки шумо ҷустуҷӯ мекардед, пешниҳод мекунад! Пайванд ба сайт бонк:')
                    bot.send_message(message.chat.id, websites[banks_tj.index(check(loan_user, language)['Bank id'].values[0])])
                    set_state(message.chat.id, session_handler, config.States.ACTION.value)
                
                elif get_language(message.chat.id, session_handler) == 'Russian':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Помощь с кредитом")
                    item2 = types.KeyboardButton("Курс валют")
                    item3 = types.KeyboardButton("Подать заявку на кредит")
                    item4 = types.KeyboardButton("Назад")
                    markup.add(item1)
                    markup.add(item2)
                    markup.add(item3)
                    markup.add(item4)

                    bot.send_message(message.chat.id, "Вот результаты подходящие вашему запросу:", reply_markup=markup)
                    bot.send_photo(message.chat.id, open('result.png', 'rb'))
                    bot.send_message(message.chat.id, check(loan_user, language)['Bank id'].values[0] + ' предлагает самые низкие процентные ставки по кредиту, который вы искали! Ссылка на сайт банка:')
                    bot.send_message(message.chat.id, websites[banks_ru.index(check(loan_user, language)['Bank id'].values[0])])
                    set_state(message.chat.id, session_handler, config.States.ACTION.value)

                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Help with a loan")
                    item2 = types.KeyboardButton("Exchange Rates")
                    item3 = types.KeyboardButton("Apply for loan")
                    item4 = types.KeyboardButton("Back")
                    markup.add(item1)
                    markup.add(item2)
                    markup.add(item3)
                    markup.add(item4)

                    bot.send_message(message.chat.id, "Here are the results for your query:", reply_markup=markup)
                    bot.send_photo(message.chat.id, open('result.png', 'rb'))
                    bot.send_message(message.chat.id, check(loan_user, language)['Bank id'].values[0] + ' offers lowest interest rates for the loan that your were searching! Link to bank website:')
                    bot.send_message(message.chat.id, websites[banks_en.index(check(loan_user, language)['Bank id'].values[0])])
                    set_state(message.chat.id, session_handler, config.States.ACTION.value)

            else:
                if language == 'Tajik':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Кӯмак бо қарз")
                    item2 = types.KeyboardButton("Мубодилаи асъор")
                    item3 = types.KeyboardButton("Ариза ба қарз")
                    item4 = types.KeyboardButton("Бозгашт")
                    markup.add(item1)
                    markup.add(item2)
                    markup.add(item3)
                    markup.add(item4)

                    if loan_user[0] == 'consumer loan':
                        if loan_user[1] == 'tjs':
                            if loan_user[3]>48:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                            elif loan_user[2]>15000:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")
                        else:
                            if loan_user[3]>48:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                            elif loan_user[2]>1500:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")
                    else:
                        if loan_user[1] == 'tjs':
                            if loan_user[3]>60:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                            elif loan_user[2]>250000:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")
                        else:
                            if loan_user[3]>60:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                            elif loan_user[2]>25000:
                                bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")

                    bot.send_message(message.chat.id, "Лутфан боз сар кунед", reply_markup=markup)
                    set_state(message.chat.id, session_handler, config.States.ACTION.value)

                elif language == 'Russian':
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Помощь с кредитом")
                    item2 = types.KeyboardButton("Курс валют")
                    item3 = types.KeyboardButton("Подать заявку на кредит")
                    item4 = types.KeyboardButton("Назад")
                    markup.add(item1)
                    markup.add(item2)
                    markup.add(item3)
                    markup.add(item4)

                    if loan_user[0] == 'consumer loan':
                        if loan_user[1] == 'tjs':
                            if loan_user[3]>48:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                            elif loan_user[2]>15000:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")
                        else:
                            if loan_user[3]>48:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                            elif loan_user[2]>1500:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")
                    else:
                        if loan_user[1] == 'tjs':
                            if loan_user[3]>60:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                            elif loan_user[2]>250000:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")
                        else:
                            if loan_user[3]>60:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                            elif loan_user[2]>25000:
                                bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")

                    bot.send_message(message.chat.id, "Пожалуйста начните еще раз", reply_markup=markup)
                    set_state(message.chat.id, session_handler, config.States.ACTION.value)

                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Help with a loan")
                    item2 = types.KeyboardButton("Exchange Rates")
                    item3 = types.KeyboardButton("Apply for loan")
                    item4 = types.KeyboardButton("Back")
                    markup.add(item1)
                    markup.add(item2)
                    markup.add(item3)
                    markup.add(item4)

                    if loan_user[0] == 'consumer loan':
                        if loan_user[2] == 'tjs':
                            if loan_user[3]>48:
                                bot.send_message(message.chat.id, "Banks don't lend for that duration")
                            elif loan_user[2]>15000:
                                bot.send_message(message.chat.id, "Banks don't lend for that amount")
                        else:
                            if loan_user[3]>48:
                                bot.send_message(message.chat.id, "Banks don't lend for that duration")
                            elif loan_user[2]>1500:
                                bot.send_message(message.chat.id, "Banks don't lend for that amount")
                    else:
                        if loan_user[2] == 'tjs':
                            if loan_user[3]>60:
                                bot.send_message(message.chat.id, "Banks don't lend for that duration")
                            elif loan_user[2]>250000:
                                bot.send_message(message.chat.id, "Banks don't lend for that amount")
                        else:
                            if loan_user[3]>60:
                                bot.send_message(message.chat.id, "Banks don't lend for that duration")
                            elif loan_user[2]>25000:
                                bot.send_message(message.chat.id, "Banks don't lend for that amount")
                                
                    bot.send_message(message.chat.id, "Please start again", reply_markup=markup)
                    set_state(message.chat.id, session_handler, config.States.ACTION.value)
            save_json(session_handler)

    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)
            
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            set_state(message.chat.id, session_handler, config.States.LOAN_DURATION.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_SELECT.value)
def apply(message):
    global session_handler
    if get_language(message.chat.id, session_handler) == 'Tajik':
        if message.text in ["Амонатбонк", "Коммерс Бонки Точикистон"]:
            session_handler[message.chat.id][4].append(message.text)

            bot.send_message(message.chat.id, "Лутфан ном ва насабатонро ворид кунед")
            set_state(message.chat.id, session_handler, config.States.APPLY_NAME.value)
        elif message.text == 'Бозгашт':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Кӯмак бо қарз")
            item2 = types.KeyboardButton("Мубодилаи асъор")
            item3 = types.KeyboardButton("Ариза ба қарз")
            item4 = types.KeyboardButton('Кӯмак')
            item5 = types.KeyboardButton("Бозгашт")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)
            markup.add(item5)

            bot.send_message(message.chat.id, "Ман ба кор таёрам!\nМан чӣ тавр ба шумо кӯмак расонам?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Амонатбонк")
            item2 = types.KeyboardButton("Коммерс Бонки Точикистон")
            markup.add(item1)
            markup.add(item2)

            bot.send_message(message.chat.id, "Лутфан яке аз бонкҳоро интихоб кунед", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_SELECT.value)

    elif get_language(message.chat.id, session_handler) == 'Russian':
        if message.text in ["Амонатбанк", "Комерческий Банк Таджикистана"]:
            session_handler[message.chat.id][4].append(message.text)

            bot.send_message(message.chat.id, "Пожалуйста введите вашe имя и фамилию")
            set_state(message.chat.id, session_handler, config.States.APPLY_NAME.value)
        
        elif message.text =='Назад':
            #Keyboard inline - russian
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Помощь с кредитом")
            item2 = types.KeyboardButton("Курс валют")
            item3 = types.KeyboardButton("Подать заявку на кредит")
            item4 = types.KeyboardButton("Помощь")
            item5 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)
            markup.add(item5)

            bot.send_message(message.chat.id, "Я готов к работе!\nЧем могу я вам помочь?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)
        
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Амонатбанк")
            item2 = types.KeyboardButton("Комерческий Банк Таджикистана")
            markup.add(item1)
            markup.add(item2)

            bot.send_message(message.chat.id, "Пожалуйста выберите один из банков", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_SELECT.value)

    else:
        if message.text in ["Amonatbank", "Commerce Bank Tajikistan"]:
            session_handler[message.chat.id][4].append(message.text)

            bot.send_message(message.chat.id, "Please enter your first and last name")
            set_state(message.chat.id, session_handler, config.States.APPLY_NAME.value)
        elif message.text == 'Back':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Help with a loan")
            item2 = types.KeyboardButton("Exchange Rates")
            item3 = types.KeyboardButton("Apply for loan")
            item4 = types.KeyboardButton("Help")
            item5 = types.KeyboardButton("Back")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            markup.add(item4)
            markup.add(item5)

            bot.send_message(message.chat.id, "I am ready to work!\nHow can i help you", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.ACTION.value)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Amonatbank")
            item2 = types.KeyboardButton("Commerce Bank Tajikistan")
            markup.add(item1)
            markup.add(item2)

            bot.send_message(message.chat.id, "Please select one of the banks", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_SELECT.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_NAME.value)
def apply_name(message):
    name = message.text.split(' ')[0]
    surname = message.text.split(' ')[1]
    session_handler[message.chat.id][4].append(name)
    session_handler[message.chat.id][4].append(surname)
    if get_language(message.chat.id, session_handler) == 'Tajik':
        bot.send_message(message.chat.id, "Лутфан рақами телефони худро ворид кунед")
        set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
    elif get_language(message.chat.id, session_handler) == 'Russian':
        bot.send_message(message.chat.id, "Пожалуйста введите ваш номер телефона")
        set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
    else:
        bot.send_message(message.chat.id, "Please enter your phone number")
        set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_PHONE.value)
def apply_phone(message):
    if message.text.isnumeric():
        if len(message.text) == 9:
            session_handler[message.chat.id][4].append(message.text)
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Лутфан акси шиносномаи худро дар формати JPG фиристед")
                set_state(message.chat.id, session_handler, config.States.APPLY_PHOTO.value)
            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "Пожалуйста отправьте фото своего пасспорта в формате JPG")
                set_state(message.chat.id, session_handler, config.States.APPLY_PHOTO.value)
            else:
                bot.send_message(message.chat.id, "Please send photo of your passport in JPG format")
                set_state(message.chat.id, session_handler, config.States.APPLY_PHOTO.value)
        else:
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Лутфан рақами дурустро ворид кунед")
                set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "Пожалуйста введите правильный номер телефона")
                set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
            else:
                bot.send_message(message.chat.id, "Please enter correct phone number")
                set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед")
            set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры")
            set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)
        else:
            bot.send_message(message.chat.id, "Please enter numbers")
            set_state(message.chat.id, session_handler, config.States.APPLY_PHONE.value)

@bot.message_handler(content_types=['photo'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_PHOTO.value)
def apply_photo(message):
    
    photo_id = message.photo[-1].file_id
    file_id = bot.get_file(photo_id)
    name, extension = os.path.splitext(file_id.file_path)

    downloaded = bot.download_file(file_id.file_path) 
    src = str(message.chat.id) + str(extension)
    with open(src, 'wb') as new:
        new.write(downloaded)

    if find_tj(src):
        session_handler[message.chat.id][4].append(src)

        if get_language(message.chat.id, session_handler) == 'Tajik':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Қарзи истеъмолӣ")
            item2 = types.KeyboardButton("Қарзи мошин")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Кабул карда шуд!")
            bot.send_message(message.chat.id, "Бо кадом мақсад шумо мехоҳед қарз гиред?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_PURPOSE.value)  
        elif get_language(message.chat.id, session_handler) == 'Russian':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Потребительский кредит")
            item2 = types.KeyboardButton("Автокредит")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Принято!")
            bot.send_message(message.chat.id, "C какой целью вы хотите взять в кредит?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_PURPOSE.value)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Consumer Loan")
            item2 = types.KeyboardButton("Car Loan")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Recieved!")
            bot.send_message(message.chat.id, "For what purpose do you want to get loan?", parse_mode="html", reply_markup=markup)   
            set_state(message.chat.id, session_handler, config.States.APPLY_PURPOSE.value)
    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан акси шиносномаи точикиатонро фиристед!")
            set_state(message.chat.id, session_handler, config.States.APPLY_PHOTO.value)
        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста отправьте фото вашего Таджикского паспорта!")
            set_state(message.chat.id, session_handler, config.States.APPLY_PHOTO.value)
        else:
            bot.send_message(message.chat.id, "Please send a photo of your Tajik passport!")
            set_state(message.chat.id, session_handler, config.States.APPLY_PHOTO.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_PURPOSE.value)
def apply_purpose(message):
    global session_handler

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('TJS')
    item2 = types.KeyboardButton('USD')
    markup.add(item1)
    markup.add(item2)

    if get_language(message.chat.id, session_handler) == 'Tajik':
        if message.text == "Қарзи истеъмолӣ" or message.text == "Қарзи мошин":
            if message.text == "Қарзи истеъмолӣ":
                session_handler[message.chat.id][4].append('consumer loan')
            else:
                session_handler[message.chat.id][3].append('car loan')

            bot.send_message(message.chat.id, "Шумо бо кадом асъор қарз гирифтан мехоҳед?",  reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Қарзи истеъмолӣ")
            item2 = types.KeyboardButton("Қарзи мошин")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Бо кадом мақсад шумо мехоҳед қарз гиред?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)
    elif get_language(message.chat.id, session_handler) == 'Russian':
        if message.text == 'Потребительский кредит' or message.text == 'Автокредит':
            if message.text == "Потребительский кредит":
                session_handler[message.chat.id][4].append('consumer loan')
            else:
                session_handler[message.chat.id][4].append('car loan')

            bot.send_message(message.chat.id, "В какой валюте вы хотите взять кредит?", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Потребительский кредит")
            item2 = types.KeyboardButton("Автокредит")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "C какой целью вы хотите взять в кредит?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)
    else:
        if message.text == 'Consumer Loan' or message.text == 'Car Loan':
            if message.text == "Consumer Loan":
                session_handler[message.chat.id][3].append('consumer loan')
            else:
                    session_handler[message.chat.id][3].append('car loan')

            bot.send_message(message.chat.id, "In what currency do you want to take a loan?", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Consumer Loan")
            item2 = types.KeyboardButton("Car Loan")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "For what purpose do you want to get loan?", parse_mode="html", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_CURRENCY.value)
def apply_currency(message):
    global session_handler

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('TJS')
    item2 = types.KeyboardButton('USD')
    markup.add(item1)
    markup.add(item2)
    
    if message.text == "TJS" or message.text == "USD":
        session_handler[message.chat.id][4].append(message.text.lower())

        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Шумо чӣ қадар қарз гирифтан мехоҳед?")
            set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Сколько вы хотите взять в кредит?")
            set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)

        else:
            bot.send_message(message.chat.id, "How much do you want to borrow?")
            set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан яке аз вариантҳоро интихоб кунед!", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста выберите один из вариантов!", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

        else:
            bot.send_message(message.chat.id, "Please select one of the options!", reply_markup=markup)
            set_state(message.chat.id, session_handler, config.States.APPLY_CURRENCY.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_AMOUNT.value)
def apply_amount(message):
    if (message.text.isnumeric() or is_float(message.text)):
        if convert_float(message.text) <= 0:
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Лутфан рақами аз сифр калонтарро ворид кунед")
                set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)

            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "Пожалуйста введите цифру больше нуля")
                set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)

            else:
                bot.send_message(message.chat.id, "Please enter a number greater than zero")
                set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)
        else:

            session_handler[message.chat.id][4].append(convert_float(message.text))
 
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Шумо ба кадом Мӯҳлат қарз гирифтан мехоҳед?\n(Лутфан, давраро бо моҳҳо ворид кунед)")
                set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "На какой срок вы хотите взять кредит?\n(Пожалуйста введите срок в месяцах)")
                set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

            else:
                bot.send_message(message.chat.id, "For how long do you want to take out a loan?\n(Please enter the period in months)")
                set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)
        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            set_state(message.chat.id, session_handler, config.States.APPLY_AMOUNT.value)

@bot.message_handler(content_types=['text'], func=lambda message: get_current_state(message.chat.id, session_handler) == config.States.APPLY_DURATION.value)
def apply_duration(message):
    global session_handler
    
    if (message.text.isnumeric() or is_float(message.text)):
        if convert_float(message.text) <= 0:
            if get_language(message.chat.id, session_handler) == 'Tajik':
                bot.send_message(message.chat.id, "Лутфан рақами аз сифр калонтарро ворид кунед")
                set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

            elif get_language(message.chat.id, session_handler) == 'Russian':
                bot.send_message(message.chat.id, "Пожалуйста введите цифру больше нуля")
                set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

            else:
                bot.send_message(message.chat.id, "Please enter a number greater than zero")
                set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)
        else:
            session_handler[message.chat.id][4].append(convert_float(message.text))
            if get_language(message.chat.id, session_handler) == 'Tajik':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Кӯмак бо қарз")
                item2 = types.KeyboardButton("Мубодилаи асъор")
                item3 = types.KeyboardButton("Ариза ба қарз")
                item4 = types.KeyboardButton("Бозгашт")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)

                name = session_handler[message.chat.id][4][1] + ' ' + session_handler[message.chat.id][4][2]
                phone = session_handler[message.chat.id][4][3]
                summ = session_handler[message.chat.id][4][7]
                photo = os.path.abspath(session_handler[message.chat.id][4][4])
                currency = session_handler[message.chat.id][4][6]
                raeson = session_handler[message.chat.id][4][5]

                if session_handler[message.chat.id][4][0] == "Амонатбонк":
                    parsers.fill_amonatbank([name, phone, summ, photo])
                elif session_handler[message.chat.id][4][0] ==  "Коммерс Бонки Точикистон":
                    parsers.fill_cbt([currency, summ, name, phone])

                bot.send_message(message.chat.id, "Дархости шумо кабул шуд. Лутфан интизор шавед, ки намояндагони бонк ба шумо занг зананд.", reply_markup=markup)
                set_state(message.chat.id, session_handler, config.States.ACTION.value)
                session_handler[message.chat.id][4] = []
            elif get_language(message.chat.id, session_handler) == 'Russian':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Помощь с кредитом")
                item2 = types.KeyboardButton("Курс валют")
                item3 = types.KeyboardButton("Подать заявку на кредит")
                item4 = types.KeyboardButton("Назад")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)

                name = session_handler[message.chat.id][4][1] + ' ' + session_handler[message.chat.id][4][2]
                phone = session_handler[message.chat.id][4][3]
                summ = session_handler[message.chat.id][4][7]
                photo = os.path.abspath(session_handler[message.chat.id][4][4])
                currency = session_handler[message.chat.id][4][6]
                raeson = session_handler[message.chat.id][4][5]

                if session_handler[message.chat.id][4][0] == "Амонатбанк":
                    parsers.fill_amonatbank([name, phone, summ, photo])
                elif session_handler[message.chat.id][4][0] ==  "Комерческий Банк Таджикистана":
                    parsers.fill_cbt([currency, summ, name, phone])

                bot.send_message(message.chat.id, str(session_handler[message.chat.id][4]))
                bot.send_message(message.chat.id, "Ваша заявка принята. Пожалуйста, дождитесь звонка представителя банка.", reply_markup=markup)
                set_state(message.chat.id, session_handler, config.States.ACTION.value)
                

                session_handler[message.chat.id][4] = []
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Help with a loan")
                item2 = types.KeyboardButton("Exchange Rates")
                item3 = types.KeyboardButton("Apply for loan")
                item4 = types.KeyboardButton("Back")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)

                name = session_handler[message.chat.id][4][1] + ' ' + session_handler[message.chat.id][4][2]
                phone = session_handler[message.chat.id][4][3]
                summ = session_handler[message.chat.id][4][7]
                photo = os.path.abspath(session_handler[message.chat.id][4][4])
                currency = session_handler[message.chat.id][4][6]
                reason = session_handler[message.chat.id][4][5]

                if session_handler[message.chat.id][4][0] == "Amonatbank":
                    parsers.fill_amonatbank([name, phone, summ, photo])
                elif session_handler[message.chat.id][4][0] ==  "Commerce Bank Tajikistan":
                    parsers.fill_cbt([currency, summ, name, phone])


                bot.send_message(message.chat.id, "Your request has been accepted. Please wait until bank representatives will call you.", reply_markup=markup)
                set_state(message.chat.id, session_handler, config.States.ACTION.value)
                session_handler[message.chat.id][4] = []

    else:
        if get_language(message.chat.id, session_handler) == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

        elif get_language(message.chat.id, session_handler) == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)
            
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            set_state(message.chat.id, session_handler, config.States.APPLY_DURATION.value)

while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        with open('log.txt', 'a') as file:
            file.write(e)


