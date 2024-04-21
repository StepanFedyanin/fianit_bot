from config.data import questions


def get_scores_text(scores_all, scores, user_id, count):
    position_icon = {
        0: '🥇 ',
        1: '🥈 ',
        2: '🥉 ',
        3: '🎖️ '
    }
    position_user = 0
    users = ['Таблица лидеров🏆 ']
    for index,score in enumerate(scores_all):
        if int(score[0]) == user_id:
            position_user = index + 1
        for i in range(len(scores)):
            if scores[i][0] == score[0]:
                seconds = scores[i][4]
                icon = position_icon[index] if index in [0, 1, 2] else position_icon[3]
                if int(score[0]) == user_id:
                    users.append(
                        f"*{index + 1}. {icon}️{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {seconds // 60} мин. и {seconds % 60} сек. *")
                else:
                    users.append(
                        f"{index + 1}. {icon}️{scores[i][1]}|Ответов {scores[i][2]}/{len(questions)}|Время {seconds // 60} мин. и {seconds % 60} сек. ")
                break
    return f'Ваше место {position_user} из {count} \n'+ '\n' +'\n'.join(users)