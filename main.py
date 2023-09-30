import os

import telebot
from telebot import types
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

name = ''
surname = ''
age = 0
chat_id = 0


@bot.message_handler(content_types=['text'])
def start(msg):
    global chat_id
    chat_id = msg.from_user.id
    if msg.text == '/reg':
        bot.send_message(msg.from_user.id, 'what is your name?')
        bot.register_next_step_handler(msg, get_name)
    else:
        bot.send_message(msg.from_user.id, 'i do not understand your msg')


def get_name(msg):
    global name
    name = msg.text
    bot.send_message(msg.from_user.id, 'what is your surname?')
    bot.register_next_step_handler(msg, get_surname)


def get_surname(msg):
    global surname
    surname = msg.text
    bot.send_message(msg.from_user.id, "how old are you?")
    bot.register_next_step_handler(msg, get_age)


def get_age(msg):
    global age
    while age == 0:
        try:
            age = int(msg.text)
        except Exception:
            bot.send_message(msg.from_user.id, 'use only numbers')
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='yes', callback_data='yes')
        key_no = types.InlineKeyboardButton(text='no', callback_data='no')
        keyboard.add(key_yes)
        keyboard.add(key_no)
        question = 'is your name %s %s and are you %d years old?' % (name, surname, age)
        bot.send_message(msg.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global age

    if call.data == 'yes':
        path = 'users_info/' + str(chat_id) + '.txt'
        f = 0
        if os.path.exists(path):
            f = open(path, 'w')
        else:
            f = open(path, 'x')
        write_user(f)
        bot.send_message(chat_id, 'you are in my db)')
        age = 0
    if call.data == 'no':
        start()


def write_user(f):
    f.write('user: %d\n' % chat_id)
    f.write('name: %s\n' % name)
    f.write('surname: %s\n' % surname)
    f.write('age: %d\n\n\n' % age)
    f.close()


bot.polling(none_stop=True, interval=0)