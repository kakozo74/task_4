import telebot
bot = telebot.TeleBot("1709600970:AAG_3ZNii1IjT62hOpRgbjML_9_SGYCr9lI")
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}', reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
        bot.send_sticker(message.from_user.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text.lower() == 'пока':
        bot.send_message(message.from_user.id, 'До скорой встречи!')
        bot.send_sticker(message.from_user.id, 'CAACAgIAAxkBAAEBJk9gcgdlwneJNNkzBAmYlra48DnyHgACTgkAAnlc4gk_IdyrDKJmzx4E')
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')
bot.polling(none_stop=True)

