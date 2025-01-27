from telebot.types import InputPollOption

import keyboards
import weather_api, utils, db
database = db.Database()

params = [["sunrise", "sunset"],
          ["temperature_2m_min", "temperature_2m_max"],
          ["apparent_temperature_min", "apparent_temperature_max"],
          ["precipitation_sum", "precipitation_probability_max"],
          ["wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"],
          ["uv_index_max"]]

text_by_param = [
    "<b>Рассвет:</b> <code>{}</code>\n<b>Закат:</b> <code>{}</code>\n\n",
    "<b>температура</b> колеблется от <code>{}</code>° до <code>{}</code>°, ",
    "<b>ощущается как</b> от <code>{}</code>° до <code>{}</code>°, ",
    "ожидается <code>{}</code>мм <b>осадков</b> с вероятностью <code>{}</code>%, ",
    "<b>ветер</b> дует со скоростью <code>{}</code>м/с с порывами до <code>{}</code>м/c в <code>{}</code> направлении, ",
    "<b>у/ф индекс:</b> <code>{}</code>, "
]


def weather(user, bot):
    user_id, user_name = user
    try:
        location = database.get_location_by_chat_id(user_id)
    except:
        bot.send_message(user_id, "Кстати, если у меня будет твоя геолокация, я смогу каждый день присылать тебе погоду. Ты знаешь что делать :)")
    cur_params = database.get_daily_params_by_user(user_id)
    w = weather_api.get_daily_weather(location[0], location[1], utils.flat_params(params, cur_params))
    # нормализация
    if "wind_direction_10m_dominant" in w:
        w["wind_speed_10m_max"] /= 4
        w["wind_gusts_10m_max"] /= 4
        w["wind_direction_10m_dominant"] = utils.get_wind_dir(w["wind_direction_10m_dominant"])

    res = f"Доброе утро, {user_name}\n\n"
    if cur_params[0] == 1:
        res += text_by_param[0].format(w['sunrise'], w['sunset'])
    res += f'Погода обещает быть {utils.get_daily_by_weathercode(w["weather_code"])}, '

    for param_id in [i for i in range(len(params)) if cur_params[i] == 1]:
        if param_id == 0:
            continue
        args = [w[a] for a in params[param_id]]
        res += text_by_param[param_id].format(*args)

    res = res[:-2]
    res += '\n\nХорошего дня!'

    bot.send_message(user_id, res)


msg_id = 0


def change_params(message, bot):
    msg = bot.send_poll(message.chat.id, 'Выберите параметры', options=[
        InputPollOption('Расссвет и закат'),
        InputPollOption('Температура'),
        InputPollOption('Ощущается как'),
        InputPollOption('Осадки'),
        InputPollOption('Скорость ветра'),
        InputPollOption('У/ф индекс')
    ], is_anonymous=False, allows_multiple_answers=True, reply_markup=keyboards.back_keyboard)
    global msg_id
    msg_id = msg.id
    bot.register_poll_answer_handler(answer_handler, utils.get_poll_handler(msg), True)


def answer_handler(answer, bot):
    p = []
    for i in range(len(params)):
        if i in answer.option_ids:
            p.append(1)
        else:
            p.append(0)
    database.update_daily_parameters(answer.user.id, p)
    bot.delete_message(answer.user.id, msg_id)
    bot.send_message(answer.user.id, text='Параметры прогноза на весь день успешно обновлены!',
                     reply_markup=keyboards.start_keyboard)
