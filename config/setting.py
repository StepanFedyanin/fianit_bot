from datetime import datetime

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BOT_TOKEN = '7139108768:AAFFUrvgdI2NLCyCInzYvickSz8bvsGqQ28'


date_str = '17.04.2024'
working_date = datetime.strptime(date_str, '%d.%m.%Y')
working_date_start = '17:06'
working_date_end = '19:50'
time_to_pass = 3600

pagination_limit = 3
