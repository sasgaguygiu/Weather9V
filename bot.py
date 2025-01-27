import telebot, daily_weather, period_weather, keyboards
import db
import utils

database = db.Database()
token = '7997271159:AAEmj8jlJ2QdHrFe7xM4pVR07GqY_pcJsYo'
bot = telebot.TeleBot(token, parse_mode='html')


@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message.from_user.first_name, message.chat.id)
    bot.send_message(message.chat.id, text='Привет! Я бот добрячок, который умеет присылать прогноз погоды. А ещё я буду писать тебе каждое утро и каждый вечер, так что не пугайся :)\n\nЧтобы начать, отправь мне свою геолокацию', reply_markup=keyboards.start_keyboard)


@bot.message_handler(func=utils.get_handler('/set_location', 'Сменить геолокацию'))
def get_location(message):
    msg = bot.send_message(message.chat.id, text='Пришлите координаты', reply_markup=keyboards.back_keyboard)
    database.set_state(message.chat.id, 4)
    bot.register_next_step_handler(msg, set_location)


def set_location(message):
    if message.content_type == 'text':
        text(message)
        return
    location = message.location
    database.set_location_by_chat_id(message.chat.id, location.latitude, location.longitude)
    bot.send_message(message.chat.id, "Геолокация обновлена успешно", reply_markup=keyboards.start_keyboard)


@bot.message_handler(func=utils.get_handler('/weather', 'Погода'))
def weather(message):
    period_weather.weather(message, bot)


@bot.message_handler(func=utils.get_handler('/change_daily_params', 'Сменить параметры утреннего прогноза'))
def change_daily_params(message):
    database.set_state(message.chat.id, 2)
    daily_weather.change_params(message, bot)


@bot.message_handler(func=utils.get_handler('/change_period_params', 'Сменить параметры общего прогноза'))
def change_period_params(message):
    database.set_state(message.chat.id, 3)
    period_weather.change_params(message, bot)


@bot.message_handler(func=utils.get_handler('/set_name', 'Сменить имя'))
def change_name1(message):
    msg = bot.send_message(message.chat.id, "Как к вам обращаться?")
    bot.register_next_step_handler(msg, change_name2)


def change_name2(message):
    database.set_user_name(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Я вас услышал")


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Настройки':
        database.set_state(message.chat.id, 1)
        bot.send_message(message.chat.id, "Вы в настройках", reply_markup=keyboards.settings_keyboard)
    elif message.text == 'Назад':
        state = database.get_state(message.chat.id)
        if state == 1:
            bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=keyboards.start_keyboard)
        elif state == 2 or state == 3 or state == 4:
            bot.send_message(message.chat.id, "Вы в настройках", reply_markup=keyboards.settings_keyboard)
        database.set_state(message.chat.id, max(0, state - 1))
    else:
        bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
