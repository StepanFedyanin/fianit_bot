from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# from config.data import questions

items = {
    False: "✅ ",
    True: ""
}


def multiple_select(question_type, answers):
    keyboard = InlineKeyboardMarkup()
    if len(answers) == 0:
        return None
    for answer in answers:
        text = answer.url
        if question_type == True:
            callback_data = f"choose_single|{answer.id}|false"
        else:
            callback_data = f"choose_multiple|{answer.id}|false"
        keyboard.row(
            InlineKeyboardButton(
                text=text,
                callback_data=callback_data
            )
        )
    if question_type == False:
        keyboard.row(
            InlineKeyboardButton(
                text="➡️ Подтвердить выбор",
                callback_data="choose_topic_ready"
            )
        )
    return keyboard


def change_multiple_select(keyboard: InlineKeyboardMarkup, key: int, condition: bool):
    new_str_condition = 'true' if not condition else 'false'
    new_keyboard = InlineKeyboardMarkup()
    for line in keyboard.inline_keyboard:
        if line[0].callback_data == "choose_topic_ready":
            continue
        if line[0].callback_data.split('|')[1] == str(key):
            new_keyboard.row(
                InlineKeyboardButton(
                    text= items[condition] + line[0].text if not condition else line[0].text[2:],
                    callback_data=f"choose_multiple|{key}|{new_str_condition}")
            )
        else:
            new_keyboard.row(line[0])

    new_keyboard.row(
        InlineKeyboardButton(
            text="➡️ Подтвердить выбор",
            callback_data="choose_topic_ready"
        )
    )
    return new_keyboard


def change_single_select(keyboard: InlineKeyboardMarkup, key: int, condition: bool):
    new_keyboard = InlineKeyboardMarkup()
    for line in keyboard.inline_keyboard:
        if line[0].callback_data == "choose_topic_ready":
            continue
        if line[0].callback_data.split('|')[1] == str(key):
            new_keyboard.row(
                InlineKeyboardButton(
                    text=items[condition] + line[0].text[2:],
                    callback_data="already_answer"
                )
            )
        else:
            new_keyboard.row(
                InlineKeyboardButton(
                    text=line[0].text,
                    callback_data="already_answer"
                )
            )
    return new_keyboard
