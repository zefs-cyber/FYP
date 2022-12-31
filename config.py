from enum import Enum


db_file = "database.vdb"

class States(Enum):

    START = '1'
    LANGUAGE = '2'
    ACTION = '3'
    LOAN = '4'
    CURRENCY_FROM = '5'
    CURRENCY_TO = '51'
    CURRENCY_AMOUNT = '52'

    OTHER = 'a'
