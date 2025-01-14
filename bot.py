import telebot, daily_weather, period_weather
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import db
import utils

database = db.Database()
token = '7997271159:AAEmj8jlJ2QdHrFe7xM4pVR07GqY_pcJsYo'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    database.add_user(message.from_user.first_name, message.chat.id)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Погода"))
    keyboard.add(KeyboardButton("Сменить геолокацию"))
    keyboard.add(KeyboardButton("Сменить параметры"))
    bot.send_message(message.chat.id, text='Привет!!!!!', reply_markup=keyboard)


@bot.message_handler(func=utils.get_handler('/set_location', 'Сменить геолокацию'))
def get_location(message):
    msg = bot.send_message(message.chat.id, text='Пришлите координаты')
    bot.register_next_step_handler(msg, set_location)


def set_location(message):
    location = message.location
    database.set_location_by_chat_id(message.chat.id, location.latitude, location.longitude)
    bot.send_message(message.chat.id, "Геолокация обновлена успешно")


@bot.message_handler(func=utils.get_handler('/weather', 'Погода'))
def weather(message):
    period_weather.weather(message, bot)


@bot.message_handler(func=utils.get_handler('/change_params', 'Сменить параметры'))
def change_params(message):
    period_weather.change_params(message, bot)


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, message.text)


bot.infinity_polling()
