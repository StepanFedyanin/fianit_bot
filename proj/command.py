import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.data import usersList, questions
from config.setting import working_date, working_date_start, working_date_end, pagination_limit, date_str, time_to_pass
from config.data import User
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp
from datetime import datetime, time, timedelta
import keyboards
from config import dp, bot
from proj.scores import get_scores_text
from proj.topics import get_question_message, get_question_correct
from aiogram.dispatcher.filters import Text
import random
import sqlite3

conn = sqlite3.connect('fianit_quiz.db')
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, name TEXT, score INTEGER, date INTEGER, finish_second INTEGER, offset INT)")
conn.commit()


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    user_id = message['from'].id
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
            (message['from'].id, message['from'].first_name, 0, '', 0, 0))
    conn.commit()
    usersList[message['from'].id] = User(message['from'].id, message['from'].first_name, 0, 0, 0, [], datetime.now(), 0,
                                         1)

    await message.answer('Правила викторины:\n\n1. Викторина состоит из 30 вопросов.\n2. У вас будет 30 минут на прохождение викторины.\n3. Место в таблице лидеров определяется по количеству правильных ответов и времени прохождения викторины.')


@dp.message_handler(Command("start_quiz"))
async def start_quiz(message: types.Message):
    user_id = message['from'].id
    current_date = datetime.now()
    current_time = current_date.time()
    start_time = time.fromisoformat(working_date_start)
    end_time = time.fromisoformat(working_date_end)
    is_already = True
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
            (message['from'].id, message['from'].first_name, 0, '', 0, 0))
    conn.commit()
    user = usersList.get(message['from'].id)
    if user:
        if len(user.answers_list) != 0:
            is_already = False

    if working_date == working_date and start_time <= current_time <= end_time and is_already:
        conn = sqlite3.connect('fianit_quiz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        k = cursor.fetchone()
        new_keyboard = InlineKeyboardMarkup()
        new_keyboard.row(
            InlineKeyboardButton(
                text="Таблица лидеров",
                callback_data="scores_callback"
            )
        )
        if k[4] != 0:
            await message.answer('Пройти викторину по правилам можно только 1 раз.', reply_markup=new_keyboard)
        else:
            object_found = False
            user = usersList.get(message['from'].id)
            if user:
                object_found = True
            if object_found == False:
                usersList[message['from'].id] = User(message['from'].id, message['from'].first_name, 0, 0, 0, [],
                                                     datetime.now(), 0, 0)
            data = get_question_message(user_id, message)
            if data['is_end'] == False:
                await message.answer(data['question_name'],
                                     reply_markup=keyboards.multiple_select(data['question_type'], data['answers']))
            else:
                user = usersList[message['from'].id]
                seconds = round((datetime.now() - user.date).total_seconds())
                conn = sqlite3.connect('fianit_quiz.db')
                cursor = conn.cursor()
                if data['not_have_time'] == True:
                    cursor.execute(
                        "REPLACE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
                        (user.id, user.name, user.score, user.date, time_to_pass, user.pagination_offset))
                else:
                    cursor.execute(
                        "REPLACE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
                        (user.id, user.name, user.score, user.date, seconds, user.pagination_offset))
                conn.commit()
                if data['not_have_time'] == True:
                    await message.answer(f'Время на прохождение викторины истекло.')
                new_keyboard = InlineKeyboardMarkup()
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Таблица лидеров",
                        callback_data=f"scores_callback"
                    )
                )
                if data['not_have_time'] == True:
                    await message.answer(
                        f'Ваш результат: {user.score} правильных из {len(questions)} вопросов. Время прохождения: {time_to_pass // 60} мин. {time_to_pass % 60} сек.',
                        reply_markup=new_keyboard)
                else:
                    await message.answer(
                        f'Ваш результат: {user.score} правильных из {len(questions)} вопросов. Время прохождения: {seconds // 60} мин. {seconds % 60} сек.',
                        reply_markup=new_keyboard)


    else:
        data = date_str[0:6] + date_str[8:]
        if is_already == False:
            await message.answer('Вы уже начали проходить викторину')
        elif current_date.replace(hour=0, minute=0, second=0, microsecond=0) > working_date:
            new_keyboard = InlineKeyboardMarkup()
            new_keyboard.row(
                InlineKeyboardButton(
                    text="Таблица лидеров",
                    callback_data=f"scores_callback"
                )
            )
            await message.answer('Викторина завершена. Вы можете посмотреть таблицу лидеров.',
                                 reply_markup=new_keyboard)
        elif current_date.replace(hour=0, minute=0, second=0, microsecond=0) < working_date:
            await message.answer(
                f'Время проведения викторины с {data + " " + working_date_start} до {data + " " + working_date_end}')
        else:
            await message.answer(
                f'Время проведения викторины с {data + " " + working_date_start} до {data + " " + working_date_end}')


@dp.message_handler(Command("scores"))
async def scores(message: types.Message):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message['from'].id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
            (message['from'].id, message['from'].first_name, 0, '', 0, 0))
    conn.commit()
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message['from'].id,))
    k = cursor.fetchone()
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == message.from_id:
            position = i + 1
            break
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * k[5] if k[5] != 0 else k[5]}")
    scores = cursor.fetchall()
    conn.commit()
    text = get_scores_text(scores_all, scores, message.from_id, len(scores_all), position)
    new_keyboard = InlineKeyboardMarkup()
    for i in scores_all:
        if int(i[0]) == message['from'].id:
            if i[5] - 1 >= 0:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    )
                )
            if (int(i[5]) + 1) * pagination_limit < len(scores_all):
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
    text = f'{text}\n\n{pagination_limit} - {k[5] + 1}/{math.ceil(len(scores_all) / pagination_limit)}'
    await message.answer(text, reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'scores_callback'))
async def scores_callback(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
            (call['from'].id, call['from'].first_name, 0, '', 0, 0))
    conn.commit()
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    k = cursor.fetchone()
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == call['from'].id:
            position = i + 1
            break
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * k[5] if k[5] != 0 else k[5]}")
    scores = cursor.fetchall()
    conn.commit()
    text = get_scores_text(scores_all, scores, call['from'].id, len(scores_all), position)
    new_keyboard = InlineKeyboardMarkup()
    for index, i in enumerate(scores_all):
        if int(scores_all[index][0]) == call['from'].id:
            if scores_all[index][5] > 0 and (scores_all[index][5] + 1) * pagination_limit < len(scores_all):
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    ),
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
            elif scores_all[index][5] > 0:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    )
                )
            elif (scores_all[index][5] + 1) * pagination_limit < len(scores_all):
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
    text = f'{text}\n\n{pagination_limit} - {k[5] + 1}/{math.ceil(len(scores_all) / pagination_limit)}'
    await call.message.answer(text, reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'scores_next'))
async def scores_next(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
            (call['from'].id, call['from'].first_name, 0, '', 0, 0))
    conn.commit()
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    k = cursor.fetchone()
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC")
    scores = cursor.fetchall()
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == call['from'].id:
            position = i + 1
            break

    for index, i in enumerate(scores):
        if int(scores[index][0]) == call['from'].id:
            cursor.execute(
                f"SELECT * FROM users ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * (scores[index][5] + 1) if (scores[index][5] + 1) != 0 else (scores[index][5] + 1)}")
            scores_list = cursor.fetchall()
            cursor.execute(
                "REPLACE INTO users (user_id,name, score, date, finish_second,  offset) VALUES (?, ?, ?, ?, ?, ?)", (
                    scores[index][0], scores[index][1], scores[index][2], scores[index][3], scores[index][4],
                    scores[index][5] + 1))
            conn.commit()

            text = get_scores_text(scores_all, scores_list, call['from'].id, len(scores_all), position)
            new_keyboard = InlineKeyboardMarkup()
            if ((scores[index][5] + 2) * pagination_limit < len(scores_all)):
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    ),
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
            else:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    )
                )
            if len(scores_list) != 0:
                print(k[5])
                text = f'{text}\n\n{pagination_limit} - {k[5] + 2}/{math.ceil(len(scores_all) / pagination_limit)}'
                await call.message.edit_text(text)
                await call.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'scores_prev'))
async def scores_prev(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
            (call['from'].id, call['from'].first_name, 0, '', 0, 0))
    conn.commit()
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    k = cursor.fetchone()
    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC")
    scores = cursor.fetchall()

    cursor.execute(
        f"SELECT * FROM users ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == call['from'].id:
            position = i + 1
            break

    scores_list = []
    for index, i in enumerate(scores):
        if int(scores[index][0]) == call['from'].id:
            if scores[index][5] - 1 >= 0:
                cursor.execute(
                    f"SELECT * FROM users ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * (scores[index][5] - 1) if (scores[index][5] - 1) != 0 else (scores[index][5] - 1)}")
                scores_list = cursor.fetchall()
                if len(scores_list) != 0:
                    cursor.execute(
                        "REPLACE INTO users (user_id,name, score, date, finish_second,  offset) VALUES (?, ?, ?, ?, ?, ?)",
                        (scores[index][0], scores[index][1], scores[index][2], scores[index][3], scores[index][4],
                         scores[index][5] - 1))
            conn.commit()
            text = get_scores_text(scores_all, scores_list, call['from'].id, len(scores_all), position)
            new_keyboard = InlineKeyboardMarkup()
            if scores[index][5] - 1 > 0:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    ),
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
            else:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
            if len(scores_list) != 0:
                text = f'{text}\n\n{pagination_limit} - {k[5]}/{math.ceil(len(scores_all) / pagination_limit)}'
                await call.message.edit_text(text)
                await call.message.edit_reply_markup(reply_markup=new_keyboard)
            break


@dp.callback_query_handler(Regexp(r'choose_multiple\|\d+\|\w{4,5}'))
async def choose_multiple(call: types.CallbackQuery, state: FSMContext):
    _, key, str_condition = call.data.split("|")
    condition = True if str_condition == "true" else False
    keyboard = call.message.reply_markup
    new_keyboard = keyboards.change_multiple_select(keyboard, key, condition)
    await call.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'choose_single\|\d+\|\w{4,5}'))
async def choose_single(call: types.CallbackQuery, state: FSMContext):
    user = usersList.get(call['from'].id)
    _, key, str_condition = call.data.split("|")
    text_answer = ''
    for line in call.message.reply_markup['inline_keyboard']:
        if line[0].callback_data.split('|')[1] == str(key):
            text_answer = f'➡️ {line[0].text}\n'

    await call.message.edit_text(f"{call.message.text}\n\nВаш ответ:\n{text_answer}")
    right_answers = get_question_correct(call['from'].id)
    data = get_question_message(call['from'].id, call.message)
    if data['is_end'] == False and data['not_have_time'] == False:
        if user.id == call['from'].id:
            if int(key) in right_answers:
                user.score = user.score + 1
                usersList[user.id] = user
        await call.message.answer(data['question_name'],
                                  reply_markup=keyboards.multiple_select(data['question_type'], data['answers']))
    else:
        seconds = round((datetime.now() - user.date).total_seconds())
        conn = sqlite3.connect('fianit_quiz.db')
        cursor = conn.cursor()
        if data['not_have_time'] == True:
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
                (user.id, user.name, user.score, user.date, time_to_pass, user.pagination_offset))
        else:
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
                (user.id, user.name, user.score, user.date, seconds, user.pagination_offset))
        conn.commit()
        if data['not_have_time'] == True:
            await call.message.answer(f'Время на прохождение викторины истекло.')
        new_keyboard = InlineKeyboardMarkup()
        new_keyboard.row(
            InlineKeyboardButton(
                text="Таблица лидеров",
                callback_data=f"scores_callback"
            )
        )
        if data['not_have_time'] == True:
            await call.message.answer(
                f'Ваш результат: {user.score} правильных из {len(questions)} вопросов. Время прохождения: {time_to_pass // 60} мин. {time_to_pass % 60} сек.',
                reply_markup=new_keyboard)
        else:
            await call.message.answer(
                f'Ваш результат: {user.score} правильных из {len(questions)} вопросов. Время прохождения: {seconds // 60} мин. {seconds % 60} сек.',
                reply_markup=new_keyboard)



@dp.callback_query_handler(Text("choose_topic_ready"))
async def selected_topics(call: types.CallbackQuery):
    user = usersList.get(call['from'].id)
    right_answers = get_question_correct(call['from'].id)
    data = get_question_message(call['from'].id, call.message)
    key_cond = []
    text_answer = ''
    for line in call.message.reply_markup.inline_keyboard:
        if line[0].callback_data == "choose_topic_ready":
            continue
        _, key, cond = line[0].callback_data.split("|")
        if cond == 'true':
            key_cond = [*key_cond, int(key)]
            text_answer = text_answer + '➡️' + line[0].text[1:] + '\n'
    if right_answers == key_cond and data['is_end'] == False and data['not_have_time'] == False:
        user.score = user.score + 1
        usersList[user.id] = user
    await call.message.edit_text(f"{call.message.text}\n\nВаш ответ:\n{text_answer}")
    if data['is_end'] == False and data['not_have_time'] == False:
        await call.message.answer(data['question_name'],
                                  reply_markup=keyboards.multiple_select(data['question_type'], data['answers']))
    else:
        seconds = round((datetime.now() - user.date).total_seconds())
        conn = sqlite3.connect('fianit_quiz.db')
        cursor = conn.cursor()
        if data['not_have_time'] == True:
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
                (user.id, user.name, user.score, user.date, time_to_pass, user.pagination_offset))
        else:
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset) VALUES (?, ?, ?, ?, ?, ?)",
                (user.id, user.name, user.score, user.date, seconds, user.pagination_offset))
        conn.commit()
        if data['not_have_time'] == True:
            await call.message.answer(f'Время на прохождение викторины истекло.')
        new_keyboard = InlineKeyboardMarkup()
        new_keyboard.row(
            InlineKeyboardButton(
                text="Таблица лидеров",
                callback_data=f"scores_callback"
            )
        )
        if data['not_have_time'] == True:
            await call.message.answer(
                f'Ваш результат: {user.score} правильных из {len(questions)} вопросов. Время прохождения: {time_to_pass // 60} мин. {time_to_pass % 60} сек.',
                reply_markup=new_keyboard)
        else:
            await call.message.answer(
                f'Ваш результат: {user.score} правильных из {len(questions)} вопросов. Время прохождения: {seconds // 60} мин. {seconds % 60} сек.',
                reply_markup=new_keyboard)
