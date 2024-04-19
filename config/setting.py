from datetime import datetime

from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BOT_TOKEN = '7094217762:AAEXQ26x6vFT4vAheRPKTYqBsmeicclW-0Q'


date_str = '19.04.2024'
working_date = datetime.strptime(date_str, '%d.%m.%Y')
working_date_start = '09:00'
working_date_end = '23:00'
time_to_pass = 1800

pagination_limit = 1
