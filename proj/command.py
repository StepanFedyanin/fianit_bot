import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config.data import questions
from config.setting import working_date, working_date_start, working_date_end, pagination_limit, date_str, time_to_pass
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp
from datetime import datetime, time, timedelta
from proj.multiple_select import multiple_select, change_multiple_select
from config import dp, bot
from proj.scores import get_scores_text
from proj.topics import get_question_message, get_question_correct
from aiogram.dispatcher.filters import Text
import sqlite3

conn = sqlite3.connect('fianit_quiz.db')
cursor = conn.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, name TEXT, score INTEGER, date INTEGER, finish_second INTEGER, offset INT, answers_id INT, answers_id_prev INT, answers_list JSON)")
conn.commit()


# id: 0
# name: 1
# score: 2
# answers_id: 6
# answers_id_prev: 7
# answers_list: 8
# date: 3
# time_finish: 4
# pagination_offset: 5

@dp.message_handler(Command("start"))
async def start(message: types.Message):
    user_id = message['from'].id
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    k = cursor.fetchone()
    if not k:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (message['from'].id, message['from'].first_name, 0, '', 0, 0, 0, 0, '[]'))
    conn.commit()
    # cursor.close()
    await message.answer(
        'Правила:\n\n Время проведения викторины - 24 апреля 2024 года с 9:00 до 24:00 по челябинскому времени (МСК +2).\nВикторину можно пройти только один раз!\nВикторина состоит из 30 вопросов.\nВремя на прохождение викторины - 30 минут.\nДля участия в викторине нажмите Меню, затем выберите /start_quiz (Пройти викторину).')


@dp.message_handler(Command("start_quiz"))
async def start_quiz(message: types.Message):
    user_id = message['from'].id

    current_date = datetime.now()
    current_time = current_date.time()
    start_time = time.fromisoformat(working_date_start)
    end_time = time.fromisoformat(working_date_end)

    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (message['from'].id, message['from'].first_name, 0, datetime.now(), 0, 0, 0, 0, '[]'))
    conn.commit()
    if working_date == working_date and start_time <= current_time <= end_time:
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        # cursor.close()
        new_keyboard = InlineKeyboardMarkup()
        new_keyboard.row(
            InlineKeyboardButton(
                text="Таблица лидеров",
                callback_data="scores_callback"
            )
        )
        if user[4] != 0:
            await message.answer('Пройти викторину по правилам можно только 1 раз.', reply_markup=new_keyboard)
        else:
            data = get_question_message(user_id, message)
            if data['is_end'] == False:
                await message.answer(data['question_name'],
                                     reply_markup=multiple_select(data['question_type'], data['answers']))
            else:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                user = cursor.fetchone()
                seconds = round((datetime.now() - user[3]).total_seconds())
                if data['not_have_time'] == True:
                    seconds = time_to_pass
                    await message.answer(f'Время на прохождение викторины истекло.')
                cursor = conn.cursor()
                cursor.execute(
                    "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list)"
                    " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (user[0], user[1], user[2], user[3], seconds, user[5], user[6], user[7], user[8]))
                conn.commit()
                conn.close()

                new_keyboard = InlineKeyboardMarkup()
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Таблица лидеров",
                        callback_data=f"scores_callback"
                    )
                )
                await message.answer(
                    f'Ваш результат: {user[2]} правильных из {len(questions)} вопросов. Время прохождения: {seconds // 60} мин. {seconds % 60} сек.',
                    reply_markup=new_keyboard)

    else:
        data = date_str[0:6] + date_str[8:]
        if current_date.replace(hour=0, minute=0, second=0, microsecond=0) <= working_date and end_time <= current_time:
            new_keyboard = InlineKeyboardMarkup()
            new_keyboard.row(
                InlineKeyboardButton(
                    text="Таблица лидеров",
                    callback_data=f"scores_callback"
                )
            )
            await message.answer('Викторина завершена. Вы можете посмотреть таблицу лидеров.',
                                 reply_markup=new_keyboard)
        else:
            await message.answer(
                f'Время проведения викторины с {data + " " + working_date_start} до {data + " " + working_date_end}')


@dp.message_handler(Command("scores"))
async def scores(message: types.Message):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message['from'].id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (message['from'].id, message['from'].first_name, 0, datetime.now(), 0, 0, 0, 0, '[]'))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (message['from'].id,))
    user = cursor.fetchone()
    cursor.execute(f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == message.from_id:
            position = i + 1
            break
    cursor.execute(
        f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * user[5] if user[5] != 0 else user[5]}")
    scores = cursor.fetchall()
    # cursor.close()
    text = get_scores_text(scores_all, scores, message.from_id, len(scores_all), position)
    new_keyboard = InlineKeyboardMarkup()
    for i in scores_all:
        if int(i[0]) == message['from'].id and user[5] - 1 > 0 or int(i[0]) == message['from'].id and(int(i[5]) + 1) * pagination_limit < len(scores_all):
            if (int(i[5]) + 1) * pagination_limit < len(scores_all) and user[5] - 1 > 0:
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
            elif user[5] - 1 > 0:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    )
                )
            elif (int(i[5]) + 1) * pagination_limit < len(scores_all):
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
            break
    await message.answer(text, reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'scores_callback'))
async def scores_callback(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    if not user:
        is_already = True
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (call['from'].id, call['from'].first_name, 0, datetime.now(), 0, 0, 0, 0, '[]'))
    conn.commit()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    cursor.execute(f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == call.message.from_id:
            position = i + 1
            break
    cursor.execute(
        f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * user[5] if user[5] != 0 else user[5]}")
    scores = cursor.fetchall()
    # cursor.close()
    text = get_scores_text(scores_all, scores, call.message.from_id, len(scores_all), position)
    new_keyboard = InlineKeyboardMarkup()
    for i in scores_all:
        if int(i[0]) == call['from'].id and user[5] - 1 > 0 or int(i[0]) == call['from'].id and(int(i[5]) + 1) * pagination_limit < len(scores_all):
            if (int(i[5]) + 1) * pagination_limit < len(scores_all) and user[5] - 1 > 0:
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
            elif user[5] - 1 > 0:
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Назад",
                        callback_data=f"scores_prev"
                    )
                )
            elif (int(i[5]) + 1) * pagination_limit < len(scores_all):
                new_keyboard.row(
                    InlineKeyboardButton(
                        text="Вперед",
                        callback_data=f"scores_next"
                    )
                )
            break
    await call.message.answer(text, reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'scores_next'))
async def scores_next(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (call['from'].id, call['from'].first_name, 0, datetime.now(), 0, 0, 0, 0, '[]'))
        conn.commit()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    cursor.execute(f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == call['from'].id:
            position = i + 1
            break
    cursor.execute(
        f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * (user[5] + 1) if (user[5] + 1) != 0 else (user[5] + 1)}")
    scores_list = cursor.fetchall()
    cursor.execute("REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (user[0], user[1], user[2], user[3], user[4], user[5] + 1, user[6], user[7], user[8]))
    conn.commit()
    # cursor.close()
    text = get_scores_text(scores_all, scores_list, call['from'].id, len(scores_all), position)
    new_keyboard = InlineKeyboardMarkup()
    if ((user[5] + 2) * pagination_limit < len(scores_all)):
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
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'scores_prev'))
async def scores_prev(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (call['from'].id, call['from'].first_name, 0, datetime.now(), 0, 0, 0, 0, '[]'))
        conn.commit()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    cursor.execute(f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC")
    scores_all = cursor.fetchall()
    position = 0
    for i in range(len(scores_all)):
        if int(scores_all[i][0]) == call['from'].id:
            position = i + 1
            break

    scores_list = []
    if user[5] - 1 >= 0:
        cursor.execute(
            f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, date ASC LIMIT {pagination_limit} OFFSET {pagination_limit * (user[5] - 1) if (user[5] - 1) != 0 else (user[5] - 1)}")
        scores_list = cursor.fetchall()
        if len(scores_list) != 0:
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user[0], user[1], user[2], user[3], user[4], user[5] - 1, user[6], user[7], user[8]))
            conn.commit()
    text = get_scores_text(scores_all, scores_list, call['from'].id, len(scores_all), position)
    new_keyboard = InlineKeyboardMarkup()
    if user[5] - 1 > 0:
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
    # cursor.close()
    if len(scores_list) != 0:
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'choose_multiple\|\d+\|\w{4,5}'))
async def choose_multiple(call: types.CallbackQuery, state: FSMContext):
    _, key, str_condition = call.data.split("|")
    condition = True if str_condition == "true" else False
    keyboard = call.message.reply_markup
    new_keyboard = change_multiple_select(keyboard, key, condition)
    await call.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.callback_query_handler(Regexp(r'choose_single\|\d+\|\w{4,5}'))
async def choose_single(call: types.CallbackQuery, state: FSMContext):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()
    conn.commit()
    right_answers = get_question_correct(call['from'].id)
    data = get_question_message(call['from'].id, call.message)
    _, key, str_condition = call.data.split("|")
    text_answer = ''
    for line in call.message.reply_markup['inline_keyboard']:
        if line[0].callback_data.split('|')[1] == str(key):
            text_answer = f'➡️ {line[0].text}\n'

    await call.message.edit_text(f"{call.message.text}\n\nВаш ответ:\n{text_answer}")

    if data['is_end'] == False and data['not_have_time'] == False:
        if int(key) in right_answers:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
            user = cursor.fetchone()
            cursor.execute(
                "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user[0], user[1], user[2] + 1, user[3], user[4], user[5], user[6], user[7], user[8]))
            conn.commit()
            cursor.close()
            conn.close()
        await call.message.answer(data['question_name'],
                                  reply_markup=multiple_select(data['question_type'], data['answers']))
    else:
        score = user[2]
        if int(key) in right_answers:
            score = score + 1

        seconds = round((datetime.now() -  datetime.strptime(user[3], "%Y-%m-%d %H:%M:%S.%f")).total_seconds())
        if data['not_have_time'] == True:
            seconds = time_to_pass
            await call.message.answer(f'Время на прохождение викторины истекло.')
        cursor = conn.cursor()
        cursor.execute(
            "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user[0], user[1], score, user[3], seconds, user[5], user[6], user[7], user[8]))
        conn.commit()
        conn.close()
        new_keyboard = InlineKeyboardMarkup()
        new_keyboard.row(
            InlineKeyboardButton(
                text="Таблица лидеров",
                callback_data=f"scores_callback"
            )
        )
        await call.message.answer(
            f'Ваш результат: {score} правильных из {len(questions)} вопросов. Время прохождения: {seconds // 60} мин. {seconds % 60} сек.',
            reply_markup=new_keyboard)


@dp.callback_query_handler(Text("choose_topic_ready"))
async def selected_topics(call: types.CallbackQuery):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
    user = cursor.fetchone()

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
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (call['from'].id,))
        user = cursor.fetchone()
        cursor.execute(
            "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user[0], user[1], user[2] + 1, user[3], user[4], user[5], user[6], user[7], user[8]))
        conn.commit()
        cursor.close()
        conn.close()
    # cursor.close()
    await call.message.edit_text(f"{call.message.text}\n\nВаш ответ:\n{text_answer}")
    if data['is_end'] == False and data['not_have_time'] == False:
        await call.message.answer(data['question_name'],
                                  reply_markup=multiple_select(data['question_type'], data['answers']))
    else:
        seconds = round((datetime.now() - user[3]).total_seconds())
        if data['not_have_time'] == True:
            seconds = time_to_pass
            await call.message.answer(f'Время на прохождение викторины истекло.')
        cursor = conn.cursor()
        cursor.execute(
            "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user[0], user[1], user[2], user[3], seconds, user[5], user[6], user[7], user[8]))
        conn.commit()
        conn.close()
        new_keyboard = InlineKeyboardMarkup()
        new_keyboard.row(
            InlineKeyboardButton(
                text="Таблица лидеров",
                callback_data=f"scores_callback"
            )
        )
        await call.message.answer(
            f'Ваш результат: {user[2]} правильных из {len(questions)} вопросов. Время прохождения: {seconds // 60} мин. {seconds % 60} сек.',
            reply_markup=new_keyboard)
