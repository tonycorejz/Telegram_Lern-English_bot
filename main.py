import telebot, requests, socks, sqlite3
from telebot import apihelper
from googletrans import Translator
from telebot import types


bot = telebot.TeleBot('1138805467:AAFKA5RAgKOyh_ewDiTIsXvsqohYl4H2wOo')
#apihelper.proxy = {'https': 'socks5h://216.144.228.130:15378'}

translator = Translator()
db = sqlite3.connect('tgbot.db')
sql = db.cursor()
sql.execute('''CREATE TABLE IF NOT EXISTS words (
    user_id INTEGER,
    word TEXT,
    status BOOLEAN
  )''')
db.commit()

user_dict = {}


class User:
    def __init__(self, word):
        self.word = word

@bot.message_handler(content_types=['text'])
def main(message):
  markup = types.ReplyKeyboardMarkup()
  game = types.KeyboardButton('Угадывать слова')
  translation = types.KeyboardButton('Перевести слово')
  help = types.KeyboardButton('Инструкция')
  markup.row(game)
  markup.row(translation)
  markup.row(help)
  question = "Что желаете сделать?"
  bot.send_message(message.from_user.id, text=question, reply_markup=markup)
  bot.register_next_step_handler(message, separator)

def separator(message):
  back = types.KeyboardButton('Назад')
  if message.text == "Угадывать слова":


    markup = types.ReplyKeyboardMarkup()
    var1 = types.KeyboardButton('')
    var2 = types.KeyboardButton('')
    var3 = types.KeyboardButton('')
    var4 = types.KeyboardButton('')
    markup.row(var1, var2)
    markup.row(var3, var4)
    question = f"Как переводится слово"
    bot.send_message(message.from_user.id, text=question, reply_markup=markup)
    bot.register_next_step_handler(message, save_word)


  elif message.text == "Перевести слово":
    bot.send_message(message.from_user.id, "Пиши мне слово, которое не знаешь как перевести")
    bot.register_next_step_handler(message, get_text_messages)
  elif message.text == "Инструкция":
    markup = types.ReplyKeyboardMarkup()
    markup.row(back)
    question = "Тут должна быть инструкция"
    bot.send_message(message.from_user.id, text=question, reply_markup=markup)
    bot.register_next_step_handler(message, main)
  else:
    bot.register_next_step_handler(message, main)

def get_text_messages(message):

  word = message.text
  user = User(word)
  user_dict[message.from_user.id] = user

  markup = types.ReplyKeyboardMarkup()
  yes = types.KeyboardButton('Да')
  no = types.KeyboardButton('Нет')
  markup.row(yes)
  markup.row(no)
  question = f"Прервод: {translator.translate(message.text, src='ru' , dest='en').text}\n\nМне запомнить слово?"
  bot.send_message(message.from_user.id, text=question, reply_markup=markup)
  bot.register_next_step_handler(message, save_word)


def save_word(message):
  if message.text == "Да":
    user = user_dict[message.from_user.id]
    db = sqlite3.connect('tgbot.db')
    sql = db.cursor()
    sql.execute(f"INSERT INTO words VALUES (?,?,?)", (message.from_user.id, user.word, 0))
    db.commit()
    question = f"Запомнил и буду задавать тебе в будущем"
  elif message.text == "Нет":
    question = "Хорошо, не запоминаю слово"

  markup = types.ReplyKeyboardMarkup()
  back = types.KeyboardButton('В меню')
  markup.row(back)
  bot.send_message(message.from_user.id, text=question, reply_markup=markup)
  bot.register_next_step_handler(message, main)

  
bot.polling(none_stop=True, interval=0)