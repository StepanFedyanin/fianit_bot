from config.data import questions


def get_scores_text(scores_all, scores, user_id, count, position):
    position_icon = {
        0: '🥇 ',
        1: '🥈 ',
        2: '🥉 ',
        3: '🎖️ '
    }
    users = ['Таблица лидеров🏆 ']
    for index,score in enumerate(scores_all):
        for i in range(len(scores)):
            if scores[i][0] == score[0]:
                seconds = scores[i][4]
                icon = position_icon[index] if index in [0, 1, 2] else position_icon[3]
                users.append(
                    f"{index + 1}. {icon}️{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {seconds // 60} мин. и {seconds % 60} сек. ")
                break
    return f'Ваше место {position} из {count} \n'+ '\n' +'\n'.join(users)