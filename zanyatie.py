#import telebot
#bot = telebot.TeleBot("1731413522:AAFmBmNeUGJ2AzLBM13cyR4job0P98L757o")

#@bot.message_handler(commands=['start','help'])
#def handel_statr_help(message):
#    bot.reply_to(message, "Я ничего не умею")

#@bot.message_handler(func=lambda message: True)
#def answer_to_message(message):
#    print(message.from_user.id)
#    if message.text == "Привет":
#        bot.send_message(message.from_user.id, "И тебе привет")
#bot.polling()

#import vk_api
#import random

#api_key = "1111111111111"
#vk = vk_api.VkApi(token=api_key)
#vk._auth_token()
#while True:
#    messanges = vk.method("messages.getConversation", {"offset": 0, "count":20, "filters": "unanswered"})
#    if messanges["count"] >= 1:
#        print(messanges)
#        id = messanges['item'][0]["last_message"]["from_id"]
#        first_name = vk.method("users.get", {'user_ids': id})[0]['first_name']
#        if messanges["items"][0]['last_message']['text'] ==
#            vk.method("messages.send", {"peer": id, "message": f"Привет", {first_name}, 'random_id': random.randint(1, 21484758)})
