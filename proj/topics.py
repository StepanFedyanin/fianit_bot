import json
import sqlite3
from datetime import datetime, time, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Text
from config.initialize import dp
from config.data import questions
import random
from config.setting import time_to_pass


def get_question_message(user_id, message):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    current_date = datetime.now()
    target_date = datetime.strptime(user[3], "%Y-%m-%d %H:%M:%S.%f")
    end_date = target_date + timedelta(seconds=time_to_pass)
    if target_date <= current_date <= end_date:
        ids_to_exclude = set([*json.loads(user[8])])
        questionsList = [question for question in [*questions] if question.id not in ids_to_exclude]
        random.shuffle(questionsList)
        if len(questionsList) != 0:
            question = questionsList[0]
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user[0], user[1], user[2], user[3], user[4], user[5], question.id, question.id, f'{[*json.loads(user[8]), question.id]}'))
            conn.commit()
            conn.close()
            return {
                "question_name": question.name,
                "question_type": question.multiple,
                "answers": question.answers,
                "is_end": False,
                "not_have_time": False
            }
        else:
            return {
                "is_end": True,
                "not_have_time": False
            }
    else:
        return {
            "not_have_time": True,
            "is_end": True,
        }


def get_question_correct(user_id):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    for index, question in enumerate(questions):
        if question.id == user[7]:
            right_answers = [i.id for i in question.answers if i.right]
            return right_answers
