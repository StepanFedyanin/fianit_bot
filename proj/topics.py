from datetime import datetime, time, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Text
from config.initialize import dp
from config.data import questions, usersList, User
import keyboards
import random
from config.setting import time_to_pass


def get_question_message(user_id, message):
    user = usersList.get(user_id)
    current_date = datetime.now()
    target_date = user.date
    end_date = target_date + timedelta(seconds=time_to_pass)
    if target_date <= current_date <= end_date:
        ids_to_exclude = set(user.answers_list)
        questionsList = [question for question in [*questions] if question.id not in ids_to_exclude]
        random.shuffle(questionsList)
        if len(questionsList) != 0:
            question = questionsList[0]
            user.answers_id = question.id,
            user.answers_id_prev = question.id
            user.answers_list = [*user.answers_list, question.id]
            usersList[user.id] = user
            return {
                "question_name": question.name,
                "question_type": question.multiple,
                "answers": question.answers,
                "is_end": False,
                "not_have_time": False
            }
        else:
            user.answers_list = user.answers_list
            usersList[user.id] = user
            return {
                "is_end": True,
                "not_have_time": False
            }
    else:
        user.answers_list = user.answers_list
        usersList[user.id] = user
        return {
            "not_have_time": True,
            "is_end": True,
        }


def get_question_correct(user_id):
    user = usersList.get(user_id)
    for index, question in enumerate(questions):
        if question.id == user.answers_id_prev:
            right_answers = [i.id for i in question.answers if i.right]
            return right_answers
