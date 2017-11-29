import os
import random
import pymorphy2
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from joke import random_joke

morph = pymorphy2.MorphAnalyzer()
TOKEN = os.environ['TOKEN']
PORT = int(os.environ.get('PORT', '8443'))
URL = os.environ['URL']

def joke(bot, update):
    words = update.message.text.replace(
            '/joke@ghetto_aggro_bot ', '').replace(
            '/joke ', '').replace(
            '/joke', '')
    if len(words) and random.randint(0, 100) < 10:
        joke = random_joke(words)
        if joke:
            update.message.reply_text(joke)

def direct_joke(bot, update):
    words = update.message.text.replace(
            '/joke@ghetto_aggro_bot ', '').replace(
            '/joke ', '').replace(
            '/joke', '')
    if len(words):
        answer = random_joke(words) or 'Чо?'
    else:
        answer = 'Не нашел глагола'
    update.message.reply_text(answer)

updater = Updater(TOKEN)

updater.dispatcher.add_handler(MessageHandler(Filters.text, joke))
updater.dispatcher.add_handler(CommandHandler('joke', direct_joke))

updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TOKEN)
updater.bot.set_webhook(URL + TOKEN)
# updater.start_polling()
updater.idle()