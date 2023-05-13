from enum import Enum


db_file = "database.vdb"

class States(Enum):

    START = '1'
    LANGUAGE = '2'
    ACTION = '3'
    LOAN_PURPOSE = '4'
    LOAN_AMOUNT = '41'
    LOAN_CURRENCY = '42'
    LOAN_DURATION = '43'
    CURRENCY_FROM = '5'
    CURRENCY_TO = '51'
    CURRENCY_AMOUNT = '52'
    APPLY_SELECT = '6'
    APPLY_PHOTO = '61'
    APPLY_PURPOSE = '62'
    APPLY_AMOUNT = '63'
    APPLY_CURRENCY = '64'
    APPLY_DURATION = '65'
    APPLY_NAME = '66'
    APPLY_PHONE = '67'

    OTHER = 'a'
