from telebot.types import InputPollOption

import weather_api, datetime, utils, db

params = [["temperature_2m"],
          ["apparent_temperature"],
          ["precipitation"],
          ["precipitation_probability"],
          ["pressure_msl"], ["visibility"],
          ["wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"]]

text_by_param = [
    "Температура: {:.1f}°",
    "Ощущается как {:.1f}°",
    "Количество осадков: {:.2f} мм",
    "Вероятность осадков: {}%",
    "Давление: {:.2f} мм ртутного столба",
    "Видимость: {} км",
    "Ветер дует со скоростью {:.1f} м/c с порывами до {:.1f} м/с в {} направлении"
]

periods = {
    "night": "Ночь ",
    "morning": "Утро ",
    "day": "День ",
    "evening": "Вечер "
}


def weather(message, bot):
    user_id = message.chat.id
    database = db.Database()
    location = database.get_location_by_chat_id(user_id)
    cur_params = database.get_daily_params_by_user(user_id)
    w = weather_api.get_periods_weather(location[0], location[1], utils.flat_params(params, cur_params))

    res = f"Погода на {datetime.datetime.now().date()}:\n"
    for period in w:
        res += periods[period] + "\n"
        pw = w[period]
        if "wind_direction_10m" in pw:
            pw["wind_direction_10m"] = utils.get_wind_dir(pw["wind_direction_10m"])

        for param_id in [i for i in range(len(params)) if cur_params[i] == 1]:
            args = [pw[a] for a in params[param_id]]
            res += text_by_param[param_id].format(*args) + "\n"

        res += '\n'
    bot.send_message(user_id, res)


def change_params(message, bot):
    msg = bot.send_poll(message.chat.id, 'Выберите параметры', options=[
        InputPollOption('Температура'),
        InputPollOption('Ощущается как'),
        InputPollOption('Количество осадков'),
        InputPollOption('Вероятность осадков'),
        InputPollOption('Атмосферное давление'),
        InputPollOption('Видимость'),
        InputPollOption('Ветер (скорость, направление)')
    ], is_anonymous=False, allows_multiple_answers=True)
    bot.register_poll_answer_handler(answer_handler, utils.get_poll_handler(msg), True)


def answer_handler(answer, bot):
    p = []
    for i in range(len(params)):
        if i in answer.option_ids:
            p.append(1)
        else:
            p.append(0)
    db.Database().update_period_parameters(answer.user.id, p)
    bot.send_message(answer.user.id, text='Параметры прогноза успешно обновлены!')
