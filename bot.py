import telebot
from telebot import types
from datetime import datetime
import config
import dbworker
import auth
import exchange_rates_rss


TOKEN = auth.TOKEN
language = ""
amount = 0
currency_from = ""
currency_to = ""

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
    global language
    with open('log.txt', 'a', encoding="utf-8") as file:
        file.write(f"{language}, {message.text}")

    if language == "Tajik":
        if message.text == "Кӯмак бо қарз":
            bot.send_message(message.chat.id, "Ин қисм ҳанӯз дар таҳия аст", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
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
            bot.send_message(message.chat.id, "Эта часть пока находится в разработке", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
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
            bot.send_message(message.chat.id, "This part is still in development", parse_mode="html")
            dbworker.set_state(message.chat.id, config.States.ACTION.value)
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

bot.polling(none_stop=True, interval=0)