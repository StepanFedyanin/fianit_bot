from datetime import datetime

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BOT_TOKEN = '7139108768:AAFFUrvgdI2NLCyCInzYvickSz8bvsGqQ28'

DATE_STR = '22.04.2024'
WORKING_DATE = datetime.strptime(DATE_STR, '%d.%m.%Y')
WORKING_DATE_START = '09:00'
WORKING_DATE_END = '21:00'
TIME_TO_PASS = 1800
CALLBACK_PHONE_NUMBER = '+155555555555'
PAGINATION_LIMIT = 10
NUMBER_OF_WINNERS = 5
