from datetime import datetime, timedelta
from timetable.data import subjects, weekdays, timetable, lesson_duration, lessons_start_time


def get_current_datetime():
    return datetime.utcnow() + timedelta(hours=3)
    # return datetime.now() + timedelta(hours=-10, minutes=40, days=0)


def get_timetable_text():
    current_datetime = get_current_datetime()
    current_time = current_datetime.time()
    last_lesson_end_time = (lessons_start_time[-1] + lesson_duration).time()

    day = get_current_datetime().isoweekday() - 1
    if day + 1 > 4:
        next_day = 0
    else:
        next_day = day + 1

    text = ''

    if day > 4:
        text += 'Сеголня нет уроков'
    elif current_time < last_lesson_end_time:
        text += '<b>Cегодня</b>\n'
        for lesson_number, subject in enumerate(timetable[day], 1):
            lesson_start_time = get_lesson_start_datetime(day, subject).time()
            if current_time < lesson_start_time:
                text += f'<i>{lesson_number})</i>  {subjects[subject]}\n'

    text += f'\n\n<b>{weekdays[next_day]}</b>\n'

    for lesson_number, subject in enumerate(timetable[day], 1):
        text += f'<i>{lesson_number})</i>  {subjects[subject]}\n'

    return text


def get_lesson_start_datetime(day: int, subject: int):
    return lessons_start_time[timetable[day].index(subject)]


def get_lesson_end_datetime(day: int, subject: int):
    return lessons_start_time[timetable[day].index(subject)] + lesson_duration


def get_lesson_info(is_now=False, is_soon=False, end_offset=False, start_offset=False, subject_name=False):
    current_datetime = get_current_datetime()
    current_time = current_datetime.time()
    day = get_current_datetime().isoweekday() - 1

    for subject in timetable[day]:

        lesson_start_datetime = get_lesson_start_datetime(day, subject)
        lesson_start_time = lesson_start_datetime.time()

        lesson_end_datetime = get_lesson_end_datetime(day, subject)
        lesson_end_time = lesson_end_datetime.time()

        if lesson_start_time < current_time < lesson_end_time:
            if end_offset:
                return round((lesson_end_datetime - current_datetime).seconds / 60)
            if is_now:
                return True
            if subject_name:
                return subjects[subject]

        if current_time < lesson_start_time and round((lesson_start_datetime - current_datetime).seconds / 60) <= 15:
            if start_offset:
                return round((lesson_start_datetime - current_datetime).seconds / 60)
            if is_soon:
                return True
            if subject_name:
                return subjects[subject]

    return False


def get_lesson_status_text():
    subject_name = get_lesson_info(subject_name=True)
    lesson_is_now = get_lesson_info(is_now=True)
    lesson_is_soon = get_lesson_info(is_soon=True)

    text = ''

    if lesson_is_now:
        lesson_end_offset = get_lesson_info(end_offset=True)
        text = f'<b>{subject_name}</b> закончится через <b>{lesson_end_offset}</b> мин\n\n'

    if lesson_is_soon:
        lesson_start_offset = get_lesson_info(start_offset=True)
        text = f'<b>{subject_name}</b> начнётся через <b>{lesson_start_offset}</b> мин\n\n'

    return text


def get_text():
    text = get_lesson_status_text() + get_timetable_text()
    return text


if __name__ == '__main__':
    print(get_text())
