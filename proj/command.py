from config.data import usersList, questions
from config.setting import working_date, working_date_start, working_date_end
from config.data import User
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp
from datetime import datetime, time
import keyboards
from config import dp, bot
from proj.topics import get_question_message, get_question_correct
from aiogram.dispatcher.filters import Text
import random
import sqlite3

conn = sqlite3.connect('fianit_quiz.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, name TEXT, score INTEGER, date INTEGER)")
conn.commit()
    
@dp.message_handler(Command("start_quiz"))
async def start(message: types.Message):
    current_date = datetime.now()
    current_time = current_date.time()
    start_time = time.fromisoformat(working_date_start)
    end_time = time.fromisoformat(working_date_end)
    if working_date == working_date and start_time <= current_time <= end_time:
        user_id = message['from'].id
        conn = sqlite3.connect('fianit_quiz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        k = cursor.fetchone()
        if k:
            await message.answer('Вы уже проходили викторину!')
        else:
            usersList.append((User(message['from'].id, message['from'].first_name, 0, 0, [], datetime.now())))
            data = get_question_message(user_id, message)
            await message.answer(data['question_name'], reply_markup=keyboards.multiple_select(data['question_type'], data['answers']))
    else:
        if current_date.replace(hour=0, minute=0, second=0, microsecond=0) > working_date:
            await message.answer('Виктарина уже закончилась')
        elif current_date.replace(hour=0, minute=0, second=0, microsecond=0) < working_date:
            await message.answer('Виктарина начнется в будушем')
        else:
            await message.answer('Совсем скоро начнется')
    
@dp.message_handler(Command("scores"))
async def scores(message: types.Message):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users ORDER BY score DESC")
    scores = cursor.fetchall()
    conn.commit()
    position = 0
    users = ['Таблица лидеров🏆 ']
    for i in range(len(scores)):
        if int(scores[i][0]) == message.from_id:
            position = i+1

        if i == 0:
            if scores[i][3] > 60:
                users.append(
                    f"🥇{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {(scores[i][3])//60} мин. и {scores[i][3]} сек. "
                )  
            else:
                users.append(
                    f"🥇{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {scores[i][3]} сек. "
            )  
        elif i == 1:
            if scores[i][3] > 60:
                users.append(
                    f"🥈{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {(scores[i][3])//60} мин. и {scores[i][3]} сек. "
                )  
            else:
                users.append(
                    f"🥈{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {scores[i][3]} сек. "
            )
        elif i == 2:
            if scores[i][3] > 60:
                users.append(
                    
                    f"🥉{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {(scores[i][3])//60} мин. и {scores[i][3]} сек. "
                )  
            else:
                users.append(
                    f"🥉{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {scores[i][3]} сек. "
            )
        else:
            if scores[i][3] > 60:
                users.append(
                    
                    f"🎖️{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {(scores[i][3])//60} мин. и {scores[i][3]} сек. "
                )  
            else:
                users.append(
                    f"🎖️{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {scores[i][3]} сек. "
            )
    await message.answer(f'Ваше место {position} из {len(scores)} \n'+ '\n' +'\n'.join(users)) 


@dp.callback_query_handler(Regexp(r'choose_multiple\|\d+\|\w{4,5}'))
async def choose_multiple(call: types.CallbackQuery, state: FSMContext):
    _, key, str_condition = call.data.split("|")
    condition = True if str_condition == "true" else False
    keyboard = call.message.reply_markup
    new_keyboard = keyboards.change_multiple_select(keyboard, key, condition)
    await call.message.edit_reply_markup(reply_markup=new_keyboard)

@dp.callback_query_handler(Regexp(r'choose_single\|\d+\|\w{4,5}'))
async def choose_single(call: types.CallbackQuery, state: FSMContext):
    _, key, str_condition = call.data.split("|")
    text_answer = ''
    for line in call.message.reply_markup['inline_keyboard']:
        if line[0].callback_data.split('|')[1] == str(key):
            text_answer = f'{line[0].text}\n'

    await call.message.edit_text(f"{call.message.text} \n \n Ваш ответ:\n {text_answer}")
    data = get_question_message(call['from'].id, call.message)
    if data['is_end'] == False:
        await call.message.answer(data['question_name'],reply_markup=keyboards.multiple_select(data['question_type'], data['answers']))
        right_answers = data['right_answers']
        for index,i in enumerate(usersList):
            if i.id == call['from'].id:
                if int(key) in right_answers:
                    updated_user = User(i.id, i.name, i.score + 1, i.id, [*i.answers_list],i.date)
                    usersList[index] = updated_user
    else:
        for i in usersList:
            if i.id == call['from'].id:
                seconds = (datetime.now() - i.date).total_seconds()
                conn = sqlite3.connect('fianit_quiz.db')
                cursor = conn.cursor()
                cursor.execute ("INSERT OR IGNORE INTO users (user_id, name, score, date) VALUES (?, ?, ?, ?)", (i.id, i.name, i.score, seconds))
                conn.commit()

@dp.callback_query_handler(Text("choose_topic_ready"))
async def selected_topics(call: types.CallbackQuery):
    data = get_question_message(call['from'].id, call.message)
    right_answers = data['right_answers']
    for index, i in enumerate(usersList):
        if i.id == call['from'].id:
            key_cond = {}
            text_answer = ''
            for line in call.message.reply_markup.inline_keyboard:
                if line[0].callback_data == "choose_topic_ready":
                    continue
                _, key, cond = line[0].callback_data.split("|")
                if cond == 'true':
                    key_cond = [*key_cond, int(key)]
                    text_answer = text_answer + line[0].text[1:] + '\n'
            await call.message.edit_text(f"{call.message.text} \n \nВаш ответ:\n{text_answer}")
            if right_answers == key_cond:
                updated_user = User(i.id, i.name, i.score + 1, i.id, [*i.answers_list], i.date)
                usersList[index] = updated_user
            print(i.score)
    if data['is_end'] == False:
        await call.message.answer(data['question_name'], reply_markup=keyboards.multiple_select(data['question_type'], data['answers']))
    else:
        print(data)
    #     for i in usersList:
    #         if i.id == call['from'].id:
    #             seconds = (datetime.now() - i.date).total_seconds()
    #             conn = sqlite3.connect('fianit_quiz.db')
    #             cursor = conn.cursor()
    #             cursor.execute ("INSERT OR IGNORE INTO users (user_id, name, score, date) VALUES (?, ?, ?, ?)", (i.id, i.name, i.score, seconds))
    #             conn.commit()
    #             await call.message.answer(f'Ваш результат: {i.score} правильных из {len(questions)} вопросов. Время прохождения: {seconds//60} мин. {seconds%60} сек.')


