from datetime import datetime, time, timedelta

from aiogram import types
from aiogram.dispatcher.filters import Text
from config.initialize import dp
from config.data import questions, usersList, User
import keyboards
import random
from config.setting import time_to_pass


def get_question_message(user_id, message):
    for index, i in enumerate(usersList):
        if i.id == user_id:
            current_date = datetime.now()
            target_date = i.date
            end_date = target_date + timedelta(seconds=time_to_pass)

            if target_date <= current_date <= end_date:
                ids_to_exclude = set(i.answers_list)
                questionsList = [question for question in [*questions] if question.id not in ids_to_exclude]
                random.shuffle(questionsList)
                if len(questionsList) != 0:
                    question = questionsList[0]
                    if i.answers_id == 0 and i.answers_id_prev == 0:
                        updated_user = User(user_id, i.name, i.score, question.id, question.id,
                                            [*i.answers_list, question.id], i.date, i.time_finish, i.pagination_offset)
                    else:
                        updated_user = User(user_id, i.name, i.score, question.id, question.id,
                                        [*i.answers_list, question.id], i.date, i.time_finish, i.pagination_offset)
                    usersList[index] = updated_user
                    return {
                        "question_name": question.name,
                        "question_type": question.multiple,
                        "answers": question.answers,
                        "is_end": False,
                        "not_have_time": False
                    }
                else:
                    updated_user = User(user_id, i.name, i.score, i.answers_id, i.answers_id, [*i.answers_list],
                                        i.date, i.time_finish, i.pagination_offset)
                    usersList[index] = updated_user
                    print(updated_user)
                    return {
                        "is_end": True,
                        "not_have_time": False
                    }
            else:
                updated_user = User(user_id, i.name, i.score, i.answers_id, i.answers_id, [*i.answers_list],
                                    i.date, i.time_finish, i.pagination_offset)
                usersList[index] = updated_user
                return {
                    "not_have_time": True,
                    "is_end": True,
                }


def get_question_correct(user_id):
    for index, i in enumerate(usersList):
        if i.id == user_id:
            for index, question in enumerate(questions):
                if question.id == i.answers_id_prev:
                    right_answers = [i.id for i in question.answers if i.right]
                    return right_answers
