from aiogram import types
from aiogram.dispatcher.filters import Text
from config.initialize import dp
from config.data import questions, usersList, User
import keyboards
import random


def get_question_message(user_id, message):
    for index, i in enumerate(usersList):
        if i.id == user_id:
            ids_to_exclude = set(i.answers_list)
            questionsList = [question for question in [*questions] if question.id not in ids_to_exclude]
            random.shuffle(questionsList)
            if len(questionsList) != 0:
                question = questionsList[0]
                right_answers = [i.id for i in question.answers if i.right]
                if next:
                    updated_user = User(user_id, i.name, i.score, question.id, [*i.answers_list, question.id], i.date)
                    usersList[index] = updated_user
                return {"question_name": question.name, "question_type": question.multiple, "answers": question.answers,
                        "right_answers": right_answers, "is_end": False}
            else:
                return {"is_end": True, "right_answers": []}