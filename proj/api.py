import sqlite3

from config.setting import pagination_limit


def get_user(user_id):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def add_user(user):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9]))
    conn.commit()
    cursor.close()
    conn.close()


def replace_user(user):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    cursor.execute(
        "REPLACE INTO users (user_id, name, score, date, finish_second, offset, answers_id, answers_id_prev, answers_list)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8]))
    conn.commit()
    conn.close()


def get_scores(offset = None):
    conn = sqlite3.connect('fianit_quiz.db')
    cursor = conn.cursor()
    if offset is not None:
        cursor.execute(
            f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, finish_second ASC LIMIT {pagination_limit} OFFSET {pagination_limit * offset if offset != 0 else offset}")
        scores = cursor.fetchall()
    else:
        cursor.execute(f"SELECT * FROM users WHERE finish_second > 0 ORDER BY score DESC, finish_second ASC")
        scores = cursor.fetchall()
    return scores
