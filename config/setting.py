from datetime import datetime

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BOT_TOKEN = '7139108768:AAFFUrvgdI2NLCyCInzYvickSz8bvsGqQ28'


date_str = '18.04.2024'
working_date = datetime.strptime(date_str, '%d.%m.%Y')
working_date_start = '10:00'
working_date_end = '20:00'
time_to_pass = 1800

pagination_limit = 10
