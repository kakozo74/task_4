import sqlite3 as sq
import telebot
from newsapi import NewsApiClient

keyboardstart = telebot.types.ReplyKeyboardMarkup()
keyboardstart.add('/Смотреть_новости_по_подпискам', '/Смотреть_новости_по_тегам', '/Добавить_тег', '/Удалить_тег', '/Выберем_новости_по_категории?', '/Отписаться_от_категории')
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.add('/Зарегестрируемся!')
keyboard2 = telebot.types.ReplyKeyboardMarkup()
keyboard2.add('/Выберем_новости_по_категории?')
keyboard3 = telebot.types.ReplyKeyboardMarkup()
keyboard3.add('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
keyboard4 = telebot.types.ReplyKeyboardMarkup()
keyboard4.add('/Смотреть_новости_по_подпискам')
keyboard5 = telebot.types.ReplyKeyboardMarkup()
keyboard5.add('/Смотреть_новости_по_подпискам', '/Добавить_тег', '/Отписаться_от_категории')
keyboard6 = telebot.types.ReplyKeyboardMarkup()
keyboard6.add('/Смотреть_новости_по_подпискам', '/Добавить_тег', '/Отписаться_от_категории', '/Смотреть_новости_по_тегам')
keyboard7 = telebot.types.ReplyKeyboardMarkup()
keyboard7.add('/Смотреть_новости_по_тегам', '/Добавить_тег', '/Удалить_тег')


conn = sq.connect('news_users.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE if NOT EXISTS "users" ("id" INTEGER NOT NULL UNIQUE, "user_id" INTEGER NOT NULL 
                    UNIQUE, PRIMARY KEY("id" AUTOINCREMENT));''')
cursor.execute('''CREATE TABLE if NOT EXISTS "categories" ("id" INTEGER NOT NULL UNIQUE, "user_id" INTEGER NOT NULL,
                    "news_categories" TEXT, PRIMARY KEY("id" AUTOINCREMENT));''')
cursor.execute('''CREATE TABLE if NOT EXISTS "keywords" ("id" INTEGER NOT NULL UNIQUE, "user_id" INTEGER NOT NULL,
                    "news_keywords" TEXT, PRIMARY KEY("id" AUTOINCREMENT));''')

conn.commit()
conn.close()

bot = telebot.TeleBot('1709600970:AAG_3ZNii1IjT62hOpRgbjML_9_SGYCr9lI', parse_mode=None)  #Убрать токен
api = NewsApiClient(api_key='6a674cae33ec44c885bafd2fbb060894')  # Убрать ключ

available_categories = ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Привет, {message.from_user.first_name}, я новостной бот, давай зарегестрируемся и посмотрим'
                          f' новости!', reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, f'{message.from_user.first_name}, Какие то проблемы? смотри все что я умею:',
                 reply_markup=keyboardstart)

@bot.message_handler(commands=['Зарегестрируемся!'])
def register_user(message):
    con = sq.connect('news_users.db')
    cur = con.cursor()
    bot.reply_to(message, 'Теперь вы зарагестрированы', reply_markup=keyboard2)
    try:
        cur.execute('''INSERT INTO users (user_id) VALUES (?)''', (message.from_user.id,))
        con.commit()
    except sq.IntegrityError:
        bot.reply_to(message, 'Пользователь уже зарегестрирован')

    con.close()


@bot.message_handler(commands=['Добавить_тег'])
def add_keyword(message):
    cid = message.chat.id
    news_keyword = bot.send_message(cid, 'Напишите_тег_для_добавления')
    bot.register_next_step_handler(news_keyword, step_set_keyword)


def step_set_keyword(message):
    user_keyword = message.text
    con = sq.connect('news_users.db')
    cur = con.cursor()
    cur.execute('''INSERT INTO keywords (user_id, news_keywords) VALUES (?,?)''', (message.from_user.id, user_keyword,))
    con.commit()
    con.close()
    bot.reply_to(message, 'Отлично, тег добавлен, что будем делать дальше?', reply_markup=keyboard7)


@bot.message_handler(commands=['Смотреть_новости_по_тегам'])
def news_get_by_keyword(message):
    cid = message.chat.id
    con = sq.connect('news_users.db')
    cur = con.cursor()
    cur.execute('''SELECT news_keywords FROM keywords WHERE user_id = (?)''', (message.from_user.id,))
    data = cur.fetchall()
    for n in data:
        all_articles = api.get_everything(q=n[0])
        bot.send_message(cid, '/----------------------/')
        bot.send_message(cid, f'Новости по теме: {n[0]}')
        bot.send_message(cid, '/----------------------/')
        for i in range(10):
            bot.send_message(cid, all_articles['articles'][i]['url'])


@bot.message_handler(commands=['Удалить_тег'])
def keyword_delete(message):
    cid = message.chat.id
    delete_keyword = bot.send_message(cid, 'Напишите тег для удаления')
    bot.register_next_step_handler(delete_keyword, step_keyword_delete)


def step_keyword_delete(message):
    keyword_text = message.text
    con = sq.connect('news_users.db')
    cur = con.cursor()
    cur.execute('''DELETE FROM keywords WHERE user_id = (?) AND news_keywords = (?)''',
                (message.from_user.id, keyword_text,))
    con.commit()
    con.close()
    bot.reply_to(message, 'Тег удален', reply_markup=keyboardstart)


@bot.message_handler(commands=['Выберем_новости_по_категории?'])
def add_category(message):
    cid = message.chat.id
    news_cat = bot.send_message(cid, 'Какие категории вас интересуют?', reply_markup=keyboard3)
    bot.register_next_step_handler(news_cat, step_set_category)


def step_set_category(message):
    cid = message.chat.id
    user_category = message.text
    if user_category in available_categories:
        con = sq.connect('news_users.db')
        cur = con.cursor()
        cur.execute('''INSERT INTO categories (user_id, news_categories) VALUES (?,?)''', (message.from_user.id,
                                                                                           user_category,))
        con.commit()
        con.close()
        bot.reply_to(message, 'Отлично! хотите посмотреть новости по вашим подпискам?', reply_markup=keyboard4)
    else:
        bot.send_message(cid, 'Для добавления доступны только категории: business, entertainment, general, health, '
                              'science, sports, technology')


@bot.message_handler(commands=['Смотреть_новости_по_подпискам'])
def news_get_by_category(message):
    cid = message.chat.id
    con = sq.connect('news_users.db')
    cur = con.cursor()
    cur.execute('''SELECT news_categories FROM categories WHERE user_id = (?)''', (message.from_user.id,))
    data = cur.fetchall()
    for n in data:
        all_articles = api.get_top_headlines(category=n[0])
        bot.send_message(cid, '/----------------------/')
        bot.send_message(cid, f'Новости по категории: {n[0]}')
        bot.send_message(cid, '/----------------------/')
        for i in range(10):
            bot.send_message(cid, all_articles['articles'][i]['url'])
        bot.reply_to(message, 'Что дальше?', reply_markup=keyboard5)

@bot.message_handler(commands=['Отписаться_от_категории'])
def category_delete(message):
    cid = message.chat.id
    delete_category = bot.send_message(cid, 'Какую категорию вы хотите удалить?', reply_markup=keyboard3)
    bot.register_next_step_handler(delete_category, step_category_delete)


def step_category_delete(message):
    category_text = message.text
    con = sq.connect('news_users.db')
    cur = con.cursor()
    cur.execute('''DELETE FROM categories WHERE user_id = (?) AND news_categories = (?)''', (message.from_user.id,
                                                                                             category_text,))
    con.commit()
    con.close()
    bot.reply_to(message, 'Вы удалили категорию подписок, что вы хотите сделать дальше?', reply_markup=keyboard5)

bot.polling()