from telebot.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(KeyboardButton("Погода"))
start_keyboard.add(KeyboardButton("Настройки"))

settings_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
settings_keyboard.add(KeyboardButton("Сменить параметры утреннего прогноза"))
settings_keyboard.add(KeyboardButton("Сменить параметры общего прогноза"))
settings_keyboard.add(KeyboardButton("Сменить геолокацию"), KeyboardButton("Сменить имя"))
settings_keyboard.add(KeyboardButton("Назад"))

back_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
back_keyboard.add(KeyboardButton("Назад"))
