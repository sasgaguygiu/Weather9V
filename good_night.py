import telebot
import db

bot = telebot.TeleBot('7997271159:AAEmj8jlJ2QdHrFe7xM4pVR07GqY_pcJsYo')

for user in db.Database().get_all_users():
    try:
        msg = f"Спокойной ночи, {user[1]}"
        bot.send_message(user[0], msg)
    except:
        pass