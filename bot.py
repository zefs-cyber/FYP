
import telebot
from telebot import types
from datetime import datetime
import config
import dbworker
import auth
import exchange_rates_rss
from helpers import *


TOKEN = auth.TOKEN
language = ""
amount = 0
currency_from = ""
currency_to = ""
loan_user = []

ex = exchange_rates_rss.exchange_rates()
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def welcome(message):
    welcome_msg = f"Привет {message.from_user.first_name}!\nКакой язык вы предпочитаете?"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🇹🇯 Tajik")
    item2 = types.KeyboardButton("🇷🇺 Russian")
    item3 = types.KeyboardButton("🇬🇧 English")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)

    bot.send_message(message.chat.id, welcome_msg, parse_mode = "html", reply_markup=markup)
    dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.LANGUAGE.value)
def get_language(message):
    global language
    if message.text[3:] == "Tajik":
        language = message.text[3:]

        #Keyboard inline - tajik
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Кӯмак бо қарз")
        item2 = types.KeyboardButton("Мубодилаи асъор")
        item3 = types.KeyboardButton("Бозгашт")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.send_message(message.chat.id, "Ман ба кор таёрам!\nМан чӣ тавр ба шумо кӯмак расонам?", parse_mode="html", reply_markup=markup)
        dbworker.set_state(message.chat.id, config.States.ACTION.value)
    elif message.text[3:] == "Russian":
        language = message.text[3:]
        
        #Keyboard inline - russian
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Помощь с кредитом")
        item2 = types.KeyboardButton("Курс валют")
        item3 = types.KeyboardButton("Назад")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.send_message(message.chat.id, "Я готов к работе!\nЧем могу я вам помочь?", parse_mode="html", reply_markup=markup)
        dbworker.set_state(message.chat.id, config.States.ACTION.value)
    elif message.text[3:] == "English":
        language = message.text[3:]

        #Keyboard inline - english
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Help with a loan")
        item2 = types.KeyboardButton("Exchange Rates")
        item3 = types.KeyboardButton("Back")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)

        bot.send_message(message.chat.id, "I am ready to work!\nHow can i help you", parse_mode="html", reply_markup=markup)
        dbworker.set_state(message.chat.id, config.States.ACTION.value)
    else:
        if message.text[3:] == "Tajik":
            bot.send_message(message.chat.id, "Ман нафаҳмидам, ки шумо чӣ дар назар доред!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)
        elif message.text[3:] == "Russian":
            bot.send_message(message.chat.id, "Я не понял, что вы имеету в виду!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)
        elif message.text[3:] == "English":
            bot.send_message(message.chat.id, "I don't know what you mean!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)
        else:
            bot.send_message(message.chat.id, "I don't know what you mean!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)
    
@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.ACTION.value)
def get_start(message):
    """Action State"""
    global language
    with open('log.txt', 'a', encoding="utf-8") as file:
        file.write(f"{language}, {message.text}")

    if language == "Tajik":
        if message.text == "Кӯмак бо қарз":           
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Қарзи истеъмолӣ")
            item2 = types.KeyboardButton("Қарзи мошин")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Бо кадом мақсад шумо мехоҳед қарз гиред?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_PURPOSE.value)
    
        elif message.text == "Мубодилаи асъор":
            bot.send_message(message.chat.id, "Кадом асъорро иваз кардан мехоҳед?\nМасалан: USD, RUB, KGS", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_FROM.value)

        elif message.text == "Бозгашт":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🇹🇯 Tajik")
            item2 = types.KeyboardButton("🇷🇺 Russian")
            item3 = types.KeyboardButton("🇬🇧 English")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Шумо ба кадом забон бартарӣ медиҳед?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)

        else:
            bot.send_message(message.chat.id, "Ман шуморо намефаҳмам, лутфан такрор кунед!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
            

    elif language == "Russian":
        if message.text == "Помощь с кредитом":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Потребительский кредит")
            item2 = types.KeyboardButton("Автокредит")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "C какой целью вы хотите взять в кредит?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_PURPOSE.value)

        elif message.text == "Курс валют":
            bot.send_message(message.chat.id, "Какую валюту вы хотите поменять?\nНапример: USD, RUB, KGS", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_FROM.value)
        
        elif message.text == "Назад":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🇹🇯 Tajik")
            item2 = types.KeyboardButton("🇷🇺 Russian")
            item3 = types.KeyboardButton("🇬🇧 English")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "Какой язык вы предпочитаете?", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)
        else:
            bot.send_message(message.chat.id, "Я вас не понимаю, пожалуйста повторите!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
    
    elif language == "English":
        if message.text == "Help with a loan":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Consumer Loan")
            item2 = types.KeyboardButton("Car Loan")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "For what purpose do you want to get loan?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_PURPOSE.value)

        elif message.text == "Exchange Rates":
            bot.send_message(message.chat.id, "What currency do you want to change?\nFor example: USD, RUB, KGS", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_FROM.value)

        elif message.text == "Back":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("🇹🇯 Tajik")
            item2 = types.KeyboardButton("🇷🇺 Russian")
            item3 = types.KeyboardButton("🇬🇧 English")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, "What language do you prefer?", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LANGUAGE.value)

        else:
            bot.send_message(message.chat.id, "I don't understand you, please repeat!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.ACTION.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.CURRENCY_FROM.value)
def get_currency_from(message):
    global currency_from, language
    if message.text.upper() in ex['NAMES_OTHER']: 
        currency_from = message.text.upper()
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Шумо ба кадом асъор иваз кардан мехоҳед?\nМасалан: USD, RUB, KGS", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_TO.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "На какую валюту вы хотите поменять?\nНапример: USD, RUB, KGS", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_TO.value)
        else:
            bot.send_message(message.chat.id, "To what currency do you want to change?\nFor example: USD, RUB, KGS", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_TO.value)
    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан асъори дурустро ворид кунед!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_FROM.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите правильную валюту!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_FROM.value)
        else:
            bot.send_message(message.chat.id, "Please enter the correct currency!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_FROM.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.CURRENCY_TO.value)
def get_currency_to(message):
    global currency_to, language
    if message.text.upper() in ex['NAMES_OTHER']:
        currency_to = message.text.upper()
        if language == 'Tajik':
            bot.send_message(message.chat.id, f"Шумо чанд {currency_from} мехоҳед иваз кунед?", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_AMOUNT.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, f"Сколько {currency_from} вы хотите поменять?", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_AMOUNT.value)
        else:
            bot.send_message(message.chat.id, f"How many {currency_from} do you want to change?", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_AMOUNT.value)
    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан асъори дурустро ворид кунед!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_TO.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите правильную валюту!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_TO.value)
        else:
            bot.send_message(message.chat.id, "Please enter the correct currency!", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_TO.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.CURRENCY_AMOUNT.value)
def get_currency_amount(message):
    global amount, currency_from, currency_to, language
    if message.text.isnumeric():
        amount = float(message.text)
        i1 = ex['NAMES_OTHER'].index(currency_from)
        i2 = ex['NAMES_OTHER'].index(currency_to)
        val = amount * (float(ex['UNIT'][i2]) / float(ex['RATE'][i2])) / (float(ex['UNIT'][i1]) / float(ex['RATE'][i1]))
        
        if language == 'Tajik':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Кӯмак бо қарз")
            item2 = types.KeyboardButton("Мубодилаи асъор")
            item3 = types.KeyboardButton("Бозгашт")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, f"Бо {amount}{currency_from} шумо {round(val, 2)}{currency_to} мегиред", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
        elif language == 'Russian':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Помощь с кредитом")
            item2 = types.KeyboardButton("Курс валют")
            item3 = types.KeyboardButton("Назад")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, f"За {amount}{currency_from} вы получите {round(val, 2)}{currency_to}", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Help with a loan")
            item2 = types.KeyboardButton("Exchange Rates")
            item3 = types.KeyboardButton("Back")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)

            bot.send_message(message.chat.id, f"For {amount}{currency_from} you will get {round(val, 2)}{currency_to}", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
        
    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_AMOUNT.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_AMOUNT.value)
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            dbworker.set_state(message.chat.id, config.States.CURRENCY_AMOUNT.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.LOAN_PURPOSE.value)
def get_loan_amount(message):
    global purpose
    if language == 'Tajik':
        if message.text == "Қарзи истеъмолӣ" or message.text == "Қарзи мошин":
            if message.text == "Қарзи истеъмолӣ":
                loan_user.append('consumer loan')
            else:
                loan_user.append('car loan')
            bot.send_message(message.chat.id, "Шумо чӣ қадар қарз гирифтан мехоҳед?")
            dbworker.set_state(message.chat.id, config.States.LOAN_AMOUNT.value)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Қарзи истеъмолӣ")
            item2 = types.KeyboardButton("Қарзи мошин")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "Бо кадом мақсад шумо мехоҳед қарз гиред?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_PURPOSE.value)
    elif language == 'Russian':
        if message.text == 'Потребительский кредит' or message.text == 'Автокредит':
            if message.text == "Потребительский кредит":
                loan_user.append('consumer loan')
            else:
                loan_user.append('car loan')
            bot.send_message(message.chat.id, "Сколько вы хотите взять в кредит?")
            dbworker.set_state(message.chat.id, config.States.LOAN_AMOUNT.value)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Потребительский кредит")
            item2 = types.KeyboardButton("Автокредит")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "C какой целью вы хотите взять в кредит?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_PURPOSE.value)
    else:
        if message.text == 'Consumer Loan' or message.text == 'Car Loan':
            if message.text == "Consumer Loan":
                loan_user.append('consumer loan')
            else:
                loan_user.append('car loan')
            bot.send_message(message.chat.id, "How much do you want to borrow?")
            dbworker.set_state(message.chat.id, config.States.LOAN_AMOUNT.value)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Consumer Loan")
            item2 = types.KeyboardButton("Car Loan")
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, "For what purpose do you want to get loan?", parse_mode="html", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_PURPOSE.value)




@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.LOAN_AMOUNT.value)
def get_loan_amount(message):
    if message.text.isnumeric():
        loan_user.append(int(message.text))
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('TJS')
        item2 = types.KeyboardButton('USD')
        markup.add(item1)
        markup.add(item2)
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Шумо бо кадом асъор қарз гирифтан мехоҳед?", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_CURRENCY.value)

        elif language == 'Russian':
            bot.send_message(message.chat.id, "В какой валюте вы хотите взять кредит?", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_CURRENCY.value)

        else:
            bot.send_message(message.chat.id, "In what currency do you want to take a loan?", reply_markup=markup)
            dbworker.set_state(message.chat.id, config.States.LOAN_CURRENCY.value)

    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            dbworker.set_state(message.chat.id, config.States.LOAN_AMOUNT.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            dbworker.set_state(message.chat.id, config.States.LOAN_AMOUNT.value)
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            dbworker.set_state(message.chat.id, config.States.LOAN_AMOUNT.value)


@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.LOAN_CURRENCY.value)
def get_loan_currency(message):
    if message.text == "TJS" or message.text == "USD":
        loan_user.append(message.text.lower())
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Шумо ба кадом Мӯҳлат қарз гирифтан мехоҳед?\n(Лутфан, давраро бо моҳҳо ворид кунед)")
            dbworker.set_state(message.chat.id, config.States.LOAN_DURATION.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "На какой срок вы хотите взять кредит?\n(Пожалуйста введите срок в месяцах)")
            dbworker.set_state(message.chat.id, config.States.LOAN_DURATION.value)
        else:
            bot.send_message(message.chat.id, "For how long do you want to take out a loan?\n(Please enter the period in months)")
            dbworker.set_state(message.chat.id, config.States.LOAN_DURATION.value)
    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан яке аз вариантҳоро интихоб кунед!")
            dbworker.set_state(message.chat.id, config.States.LOAN_CURRENCY.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста выберите один из вариантов!")
            dbworker.set_state(message.chat.id, config.States.LOAN_CURRENCY.value)
        else:
            bot.send_message(message.chat.id, "Please select one of the options!")
            dbworker.set_state(message.chat.id, config.States.LOAN_CURRENCY.value)

@bot.message_handler(content_types=['text'], func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.LOAN_DURATION.value)
def get_loan_currency(message):
    global loan_user
    if message.text.isnumeric():
        loan_user.append(int(message.text))
        exp_image(loan_user, language)
        print(f'{message.from_user.first_name} - image exported; {str(loan_user)}')
        if len(check(loan_user, language)) > 0:
            if language == 'Tajik':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Кӯмак бо қарз")
                item2 = types.KeyboardButton("Мубодилаи асъор")
                item3 = types.KeyboardButton("Бозгашт")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                bot.send_message(message.chat.id, "Натиҷаҳои барои талаботи шумо:", reply_markup=markup)
                bot.send_photo(message.chat.id, open('result.png', 'rb'))
                bot.send_message(message.chat.id, check(loan_user, language)['Bank id'].values[0] + ' фоизи пасттаринро барои қарзе, ки шумо ҷустуҷӯ мекардед, пешниҳод мекунад! Пйванда ба сайт бонк:')
                bot.send_message(message.chat.id, websites[banks_tj.index(check(loan_user, language)['Bank id'].values[0])])
                dbworker.set_state(message.chat.id, config.States.ACTION.value)
            elif language == 'Russian':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Помощь с кредитом")
                item2 = types.KeyboardButton("Курс валют")
                item3 = types.KeyboardButton("Назад")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)

                bot.send_message(message.chat.id, "Вот результаты подходящие вашему запросу:", reply_markup=markup)
                bot.send_photo(message.chat.id, open('result.png', 'rb'))
                bot.send_message(message.chat.id, check(loan_user, language)['Bank id'].values[0] + ' предлагает самые низкие процентные ставки по кредиту, который вы искали! Ссылка на сайт банка:')
                bot.send_message(message.chat.id, websites[banks_ru.index(check(loan_user, language)['Bank id'].values[0])])
                dbworker.set_state(message.chat.id, config.States.ACTION.value)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Help with a loan")
                item2 = types.KeyboardButton("Exchange Rates")
                item3 = types.KeyboardButton("Back")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)


                bot.send_message(message.chat.id, "Here are the results for your query:", reply_markup=markup)
                bot.send_photo(message.chat.id, open('result.png', 'rb'))
                bot.send_message(message.chat.id, check(loan_user, language)['Bank id'].values[0] + ' offers lowest interest rates for the loan that your were searching! Link to bank website:')
                bot.send_message(message.chat.id, websites[banks_en.index(check(loan_user, language)['Bank id'].values[0])])
                dbworker.set_state(message.chat.id, config.States.ACTION.value)
            
            loan_user = []

        else:
            if language == 'Tajik':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Кӯмак бо қарз")
                item2 = types.KeyboardButton("Мубодилаи асъор")
                item3 = types.KeyboardButton("Бозгашт")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)

                if loan_user[0] == 'consumer loan':
                    if loan_user[2] == 'tjs':
                        if loan_user[3]>48:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                        elif loan_user[1]>15000:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")
                    else:
                        if loan_user[3]>48:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                        elif loan_user[1]>1500:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")
                else:
                    if loan_user[2] == 'tjs':
                        if loan_user[3]>60:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                        elif loan_user[1]>250000:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")
                    else:
                        if loan_user[3]>60:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин муддат қарз намедиҳанд")
                        elif loan_user[1]>25000:
                            bot.send_message(message.chat.id, "Бонкҳо барои ин маблағ қарз намедиҳанд")

                bot.send_message(message.chat.id, "Лутфан боз сар кунед", reply_markup=markup)
                dbworker.set_state(message.chat.id, config.States.ACTION.value)

            elif language == 'Russian':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Помощь с кредитом")
                item2 = types.KeyboardButton("Курс валют")
                item3 = types.KeyboardButton("Назад")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)

                if loan_user[0] == 'consumer loan':
                    if loan_user[2] == 'tjs':
                        if loan_user[3]>48:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                        elif loan_user[1]>15000:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")
                    else:
                        if loan_user[3]>48:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                        elif loan_user[1]>1500:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")
                else:
                    if loan_user[2] == 'tjs':
                        if loan_user[3]>60:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                        elif loan_user[1]>250000:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")
                    else:
                        if loan_user[3]>60:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такой срок")
                        elif loan_user[1]>25000:
                            bot.send_message(message.chat.id, "Банки не выдают кредиты на такую сумму")

                bot.send_message(message.chat.id, "Пожалуйста начните еще раз", reply_markup=markup)
                dbworker.set_state(message.chat.id, config.States.ACTION.value)

            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Help with a loan")
                item2 = types.KeyboardButton("Exchange Rates")
                item3 = types.KeyboardButton("Back")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)

                if loan_user[0] == 'consumer loan':
                    if loan_user[2] == 'tjs':
                        if loan_user[3]>48:
                            bot.send_message(message.chat.id, "Banks don't lend for that duration")
                        elif loan_user[1]>15000:
                            bot.send_message(message.chat.id, "Banks don't lend for that amount")
                    else:
                        if loan_user[3]>48:
                            bot.send_message(message.chat.id, "Banks don't lend for that duration")
                        elif loan_user[1]>1500:
                            bot.send_message(message.chat.id, "Banks don't lend for that amount")
                else:
                    if loan_user[2] == 'tjs':
                        if loan_user[3]>60:
                            bot.send_message(message.chat.id, "Banks don't lend for that duration")
                        elif loan_user[1]>250000:
                            bot.send_message(message.chat.id, "Banks don't lend for that amount")
                    else:
                        if loan_user[3]>60:
                            bot.send_message(message.chat.id, "Banks don't lend for that duration")
                        elif loan_user[1]>25000:
                            bot.send_message(message.chat.id, "Banks don't lend for that amount")
                            
                bot.send_message(message.chat.id, "Please start again", reply_markup=markup)
                dbworker.set_state(message.chat.id, config.States.ACTION.value)
            loan_user = []

    else:
        if language == 'Tajik':
            bot.send_message(message.chat.id, "Лутфан рақам ворид кунед!")
            dbworker.set_state(message.chat.id, config.States.LOAN_DURATION.value)
        elif language == 'Russian':
            bot.send_message(message.chat.id, "Пожалуйста введите цифры!")
            dbworker.set_state(message.chat.id, config.States.LOAN_DURATION.value)
        else:
            bot.send_message(message.chat.id, "Please enter numbers!")
            dbworker.set_state(message.chat.id, config.States.LOAN_DURATION.value)


bot.polling(none_stop=True, interval=0)