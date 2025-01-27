import telebot
import daily_weather
import db

bot = telebot.TeleBot('7997271159:AAEmj8jlJ2QdHrFe7xM4pVR07GqY_pcJsYo', parse_mode="HTML")

for user in db.Database().get_all_users():
    try:
        daily_weather.weather(user, bot)
    except:
        pass