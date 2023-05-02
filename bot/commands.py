import telebot
from db import BotDB
from telebot import types
from main import Note


bot = telebot.TeleBot("6250303260:AAG6kxQ0h2WqiWIEbW14fWKKB-QUZcMl2vk")

BotDB = BotDB('list.db')
NewNote = Note

@bot.message_handler(commands = ["start"])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать!")
    bot.send_message(message.chat.id, "Я бот, который хранит информацию о важных для Вас книгах.")


@bot.message_handler(commands = ["help"])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    new_note = types.KeyboardButton('Добавить новую запись')
    old_notes = types.KeyboardButton('Посмотреть существующие')
    markup.add(new_note, old_notes)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Добавить новую запись':
            msg = bot.send_message(message.chat.id, 'Введите название:')
            bot.register_next_step_handler(msg, name_step)

        if message.text == 'Посмотреть существующие':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            best_note = types.KeyboardButton('Вывести материал(ы) с наивысшей оценкой')
            markup.add(best_note)
            bot.send_message(message.chat.id, 'Выберите действие:', reply_markup = markup)
            BotDB.get_records()
            bot.send_message(message.chat.id, BotDB.get_records())


def name_step(message):
    NewNote.name = message.text
    msg = bot.send_message(message.chat.id, 'Введите ссылку:')
    bot.register_next_step_handler(msg, link_step)


def link_step(message):
    NewNote.link = message.text
    msg = bot.send_message(message.chat.id, 'Введите Вашу оценку источнику:')
    bot.register_next_step_handler(msg, mark_step)


def mark_step(message):
    NewNote.mark = message.text
    BotDB.add_record(NewNote.name, NewNote.link, NewNote.mark)
    msg = bot.send_message(message.chat.id, '<b>Информация о введенной книге</b> \n \n<i>Название книги:</i> {}\n<i>Ссылка на книгу:</i> {}\n<i>Оценка:</i> {}'.format(NewNote.name, NewNote.link, NewNote.mark),
                           parse_mode = 'html')
    bot.register_next_step_handler(msg, help)



bot.polling(none_stop = True)