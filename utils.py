import datetime

months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
          'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']

weather_codes = {
    '0': ['Ясно', 'ясная'],
    '1': ['Преимущественно ясно', 'преимущественно ясная'],
    '2': ['Малооблачно', 'малооблачная'],
    '3': ['Облачно', 'облачная'],
    '45': ['Туман', 'туманная'],
    '48': ['Сильный туман', 'очень туманная'],
    '51': ['Лёгкая морось', 'немного моросящая'],
    '53': ['Средняя морось', 'моросящая'],
    '55': ['Сильная морось', 'сильно моросящая'],
    '56': ['Лёгкая ледяная морось', 'немного ледяно-моросящая'],
    '57': ['Ледяная морось', 'ледяно-моросящая'],
    '61': ['Слабый дождь', 'немного дождливая'],
    '63': ['Дождь', 'дождливая'],
    '65': ['Сильный дождь', 'очень дождливая'],
    '66': ['Слабый ледяной дождь', 'немного ледяно-дождливая'],
    '67': ['Ледяной дождь', 'ледяно-дождливая'],
    '71': ['Лёгкий снег', 'немного снежная'],
    '73': ['Снег', 'снежная'],
    '75': ['Сильный снег', 'очень снежная'],
    '77': ['Большой снег', 'большеснежная'],
    '80': ['Лёгкий ливень', 'немного ливневая'],
    '81': ['Ливень', 'ливневая'],
    '82': ['Сильный ливень', 'очень ливневая'],
    '85': ['Лёгкий снегопад', 'немного снегопадная'],
    '86': ['Снегопад', 'снегопадная'],
    '95': ['Слабая гроза', 'немного грозовая'],
    '96': ['Гроза', 'грозовая'],
    '99': ['Гроза с градом', 'градо-грозовая'],
}


def get_poll_handler(message):
    return lambda poll_answer: poll_answer.poll_id == message.poll.id


def get_handler(*args):
    return lambda message: message.text in args


def flat_params(params, prms):
    res = []

    for i in range(len(prms)):
        if prms[i] == 1:
            if type(params[i]) == list:
                res += params[i]
            else:
                res += [params[i]]

    return res


def get_date():
    month, day = str(datetime.datetime.now().date()).split('-')[1:]
    return f"{day} {months[int(month) - 1]}"


def get_wind_dir(angle):
    if angle >= 335 or angle < 25:
        return "северном"
    elif 25 <= angle < 65:
        return "северо\-восточном"
    elif 65 <= angle < 115:
        return "восточном"
    elif 115 <= angle < 155:
        return "юго\-восточном"
    elif 155 <= angle < 205:
        return "южном"
    elif 205 <= angle < 245:
        return "юго\-западном"
    elif 245 <= angle < 295:
        return "западном"
    else:
        return "северном"


def get_period_by_weathercode(code):
    return get_weather_by_code(code)[0]

def get_daily_by_weathercode(code):
    return get_weather_by_code(code)[1]

def get_weather_by_code(code):
    return weather_codes[str(code)]
