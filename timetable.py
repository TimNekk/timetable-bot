from datetime import datetime, timedelta
import os
from time import sleep

subjects = ['Английский язык',  # 0
            'Биология',  # 1
            'География',  # 2
            'Информатика',  # 3
            'История',  # 4
            'Литература',  # 5
            'Математика',  # 6
            'Обществознание',  # 7
            'ОБЖ',  # 8
            'Русский язык',  # 9
            'Физика',  # 10
            'Физ-ра',  # 11
            'Химия',  # 12
            'Практикум по математике',  # 13
            'Астрономия',  # 14
            'Индивидуальный проект',  # 15
            'Практикум по обществознанию',  # 16
            'Обществознание 2',  # 17
            ]

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница']

timetable = [[9, 0, 7, 10, 6, 5, 3],  # понедельник
             [1, 11, 0, 8, 6, 9, 5],  # вторник
             [6, 10, 12, 4, 0, 5, 14],  # среда
             [7, 6, 12, 9, 11, 17],  # четверг
             [15, 1, 0, 6, 13, 4, 16]]  # пятница

lesson_duration = timedelta(minutes=45)
lessons_start_time = ['8:30', '9:30', '10:30', '11:30', '12:30', '13:30', '14:30']

for time in lessons_start_time:
    lessons_start_time[lessons_start_time.index(time)] = datetime.strptime(time, '%H:%M')


def get_current_time():
    return datetime.utcnow() + timedelta(hours=3)
    # return datetime.now() + timedelta(hours=-14, days=0)


def show_all_subjects():
    for subject in subjects:
        print(str(subjects.index(subject)) + ') ' + subject)


def get_next_lessons_str(day=get_current_time().isoweekday()):
    now_time = get_current_time().time()
    lest_lesson_end_time = (lessons_start_time[-1] + lesson_duration).time()
    text = ''
    emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣']

    day -= 1
    if day > 4:
        text += 'Сеголня нет уроков'
    elif now_time < lest_lesson_end_time:
        text += '<b>Cегодня</b>\n'
        i = 1
        for subject in timetable[day]:

            lesson_start_time = lessons_start_time[timetable[day].index(subject)].time()

            if now_time < lesson_start_time:
                text += f'{emojis[i]} {subjects[subject]}\n'
            i += 1

    day += 1
    if day > 4:
        day = 0
    i = 1
    text += f'\n\n<b>{weekdays[day]}</b>\n'
    for subject in timetable[day]:
        text += f'{emojis[i]} {subjects[subject]}\n'
        i += 1

    return text


def get_current_lesson_str(day=get_current_time().isoweekday()):
    now_time = get_current_time()

    day -= 1

    text = ''
    if not day > 4:
        for subject in timetable[day]:

            lesson_start_time = lessons_start_time[timetable[day].index(subject)]
            lesson_end_time = (lessons_start_time[timetable[day].index(subject)] + lesson_duration)

            if lesson_start_time.time() < now_time.time() < lesson_end_time.time():
                end_time = round((lesson_end_time - now_time).seconds / 60)
                text = f'<b>{subjects[subject]}</b> ' \
                       f'закончится через <b>{end_time}</b> мин\n\n'
                return text
            elif now_time.time() < lesson_start_time.time() and round((lesson_start_time - now_time).seconds / 60) < 61:
                start_time = round((lesson_start_time - now_time).seconds / 60)
                text = f'<b>{subjects[subject]}</b> начнётся через <b>{start_time}</b> мин\n\n'
                return text
    return ''




def get_time_str():
    now_time = get_current_time()
    return 'Время: ' + datetime.strftime(now_time, '%H:%M') + '\n\n'


def create_message():
    text = get_current_lesson_str() + get_next_lessons_str()
    return text


if __name__ == '__main__':
    print(create_message())
    # print(get_current_lesson_str())