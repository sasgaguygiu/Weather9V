from telebot.types import InputPollOption

import keyboards
import weather_api, utils, db
database = db.Database()

params = [["temperature_2m"],
          ["apparent_temperature"],
          ["precipitation"],
          ["precipitation_probability"],
          ["pressure_msl"], ["visibility"],
          ["wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"],
          ["sunshine_duration"], ["relative_humidity_2m"]]

text_by_param = [
    "Температура: <code>{:.1f}</code>°",
    "<i>Ощущается</i> как <code>{:.1f}</code>°",
    "Количество <i>осадков</i>: <code>{:.2f}</code> мм",
    "Вероятность <i>осадков</i>: <code>{}</code>%",
    "Давление: <code>{:.2f}</code> мм ртутного столба",
    "Видимость: <code>{:.1f}</code> км",
    "Ветер дует <i>со скоростью</i> <code>{:.1f}</code> м/c <i>с порывами</i> до <code>{:.1f}</code> м/с в <code>{}</code> направлении",
    "Длительность солнца: <code>{:.0f}</code> cек",
    "Относительная <i>влажность</i> воздуха: <code>{:.1f}</code>%"
]

periods = {
    "night": "Ночь ",
    "morning": "Утро ",
    "day": "День ",
    "evening": "Вечер "
}


def weather(message, bot):
    user_id = message.chat.id
    try:
        location = database.get_location_by_chat_id(user_id)
    except:
        bot.send_message(user_id, "Пожалуйста пришлите геолокацию")
        return
    cur_params = database.get_period_params_by_user(user_id)
    w = weather_api.get_periods_weather(location[0], location[1], utils.flat_params(params, cur_params))

    res = f"<code>{database.get_user_name(user_id)}</code>, вот погода на {utils.get_date()}:\n"
    for period in w:
        res += f"<b>{periods[period]}</b>\n"
        pw = w[period]
        res += utils.get_period_by_weathercode(pw['weather_code']) + "\n"

        # нормализация
        if "wind_direction_10m" in pw:
            pw["wind_speed_10m"] /= 4
            pw["wind_gusts_10m"] /= 4
            pw["wind_direction_10m"] = utils.get_wind_dir(pw["wind_direction_10m"])

        # метры в километры
        if "visibility" in pw:
            pw["visibility"] /= 1000

        # гекто-паскали в мм ртутного столба
        if "pressure_msl" in pw:
            pw["pressure_msl"] /= 1.333

        for param_id in [i for i in range(len(params)) if cur_params[i] == 1]:
            args = [pw[a] for a in params[param_id]]
            res += text_by_param[param_id].format(*args) + "\n"

        res += '\n'
    bot.send_message(user_id, res)

msg_id1 = 0

def change_params(message, bot):
    msg = bot.send_poll(message.chat.id, 'Выберите параметры', options=[
        InputPollOption('Температура'),
        InputPollOption('Ощущается как'),
        InputPollOption('Количество осадков'),
        InputPollOption('Вероятность осадков'),
        InputPollOption('Атмосферное давление'),
        InputPollOption('Видимость'),
        InputPollOption('Ветер (скорость, направление)'),
        InputPollOption('Количество солнца'),
        InputPollOption('Относительная влажность'),
    ], is_anonymous=False, allows_multiple_answers=True, reply_markup=keyboards.back_keyboard)
    global msg_id1
    msg_id1 = msg.id
    bot.register_poll_answer_handler(answer_handler, utils.get_poll_handler(msg), True)

def answer_handler(answer, bot):
    p = []
    for i in range(len(params)):
        if i in answer.option_ids:
            p.append(1)
        else:
            p.append(0)
    database.update_period_parameters(answer.user.id, p)
    bot.delete_message(answer.user.id, msg_id1)
    bot.send_message(answer.user.id, text='Параметры прогноза успешно обновлены!', reply_markup=keyboards.start_keyboard)
