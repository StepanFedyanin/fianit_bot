import json
from datetime import datetime, time, timedelta

from config.data import questions
import random
from config.setting import TIME_TO_PASS
from proj.api import get_user, replace_user


def get_question_message(user_id, message):
    user = get_user(user_id)
    current_date = datetime.now()
    target_date = datetime.strptime(user[3], "%Y-%m-%d %H:%M:%S.%f")
    end_date = target_date + timedelta(seconds=TIME_TO_PASS)
    if target_date <= current_date <= end_date:
        ids_to_exclude = set([*json.loads(user[8])])
        questionsList = [question for question in [*questions] if question.id not in ids_to_exclude]
        random.shuffle(questionsList)
        if len(questionsList) != 0:
            question = questionsList[0]
            print(len(questionsList), question.id, ids_to_exclude)
            params = (user[0], user[1], user[2], user[3], user[4], user[5], question.id, question.id, f'{[*json.loads(user[8]), question.id]}', user[9])
            replace_user(params)
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
    user = get_user(user_id)
    for index, question in enumerate(questions):
        if question.id == user[7]:
            right_answers = [i.id for i in question.answers if i.right]
            return right_answers
