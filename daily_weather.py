from telebot.types import InputPollOption

import weather_api, utils, db

params = [["temperature_2m_min", "temperature_2m_max"],
          ["apparent_temperature_min", "apparent_temperature_max"],
          ["sunrise", "sunset"],
          ["uv_index_max"],
          ["precipitation_sum"],
          ["precipitation_probability_max"],
          ["wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"]]

text_by_param = [
    "Температура колеблется от {}° до {}°",
    "Ощущается от {}° до {}°",
    "Рассвет: {}, закат: {}",
    "У/ф индекс: {}",
    "Количество осадков: {}мм",
    "Вероятность осадков: {}%",
    "Ветер дует со скоростью {}м/с с порывами до {}м/c в {} направлении"
]

def weather(message, bot):
    user_id = message.chat.id
    database = db.Database()
    location = database.get_location_by_chat_id(user_id)
    cur_params = database.get_daily_params_by_user(user_id)
    w = weather_api.get_daily_weather(location[0], location[1], utils.flat_params(params, cur_params))
    if "wind_direction_10m_dominant" in w:
        w["wind_direction_10m_dominant"] = utils.get_wind_dir(w["wind_direction_10m_dominant"])

    res = "Погода на сегодня\n"

    for param_id in [i for i in range(len(params)) if cur_params[i] == 1]:
        args = [w[a] for a in params[param_id]]
        res += text_by_param[param_id].format(*args) + ". "

    bot.send_message(user_id, res)


def change_params(message, bot):
    msg = bot.send_poll(message.chat.id, 'Выберите параметры', options=[
        InputPollOption('Температура'),
        InputPollOption('Ощущается как'),
        InputPollOption('Расссвет и закат'),
        InputPollOption('У/ф индекс'),
        InputPollOption('Количество осадков'),
        InputPollOption('Вероятность осадков'),
        InputPollOption('Скорость ветра')
    ], is_anonymous=False, allows_multiple_answers=True)
    bot.register_poll_answer_handler(answer_handler, utils.get_poll_handler(msg), True)


def answer_handler(answer, bot):
    p = []
    for i in range(len(params)):
        if i in answer.option_ids:
            p.append(1)
        else:
            p.append(0)
    db.Database().update_daily_parameters(answer.user.id, p)
    bot.send_message(answer.user.id, text='Параметры прогноза на весь день успешно обновлены!')
