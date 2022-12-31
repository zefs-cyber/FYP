import exchange_rates_rss

ex = exchange_rates_rss.exchange_rates()

amount = 100
currency_from = "USD"
currency_to = "EUR"

i1 = ex['NAMES_OTHER'].index(currency_from)
i2 = ex['NAMES_OTHER'].index(currency_to)
val = amount * (float(ex['UNIT'][i2]) / float(ex['RATE'][i2])) / (float(ex['UNIT'][i1]) / float(ex['RATE'][i1]))
print(float(ex['UNIT'][i1]) * float(ex['RATE'][i1]))
print(float(ex['UNIT'][i2]) * float(ex['RATE'][i2]))
print(val)
