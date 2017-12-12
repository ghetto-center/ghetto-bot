#! /usr/bin/env python3

import os
import re
import logging
import pymorphy2
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from joke import random_joke, regex_joke, dict_joke, sticker_id, reply_sticker_id
from joke_utils import get_next_start, rnd_percent

morph = pymorphy2.MorphAnalyzer()
TOKEN = os.environ['TOKEN']
PORT = int(os.environ.get('PORT', '8443'))
URL = os.environ.get('URL')
POLL = int(os.environ.get('POLL'))
LOGLEVEL = os.environ.get('LOGLEVEL', 'CRITICAL')

CHATS = set([])

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s][%(funcName)s] %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, LOGLEVEL.upper(), None))

if not URL and not POLL:
    raise Exception(
        'There is no URL or POLL enviroment variable, just set one of')


def strip_cmd(f):
    def wrap(bot, update):
        update.message.text = re.sub('\/joke(@\w+)?', '', update.message.text)
        f(bot, update)
    return wrap


def save_chatid(f):
    def wrap(bot, update):
        CHATS.add(update.message.chat_id)
        f(bot, update)
    return wrap


@save_chatid
@strip_cmd
def joke(bot, update):
    words = update.message.text
    logger.debug('words: ' + str(words))
    if len(words):
        joke = regex_joke(words)
        if joke is None and rnd_percent(10):
            joke = random_joke(words)
        if joke:
            update.message.reply_text(joke)
            logger.debug('joke: ' + joke)
        elif rnd_percent(5):
            sticker_id = reply_sticker_id()
            update.message.reply_sticker(sticker=sticker_id)
            logger.debug('joke: ' + sticker_id)
        else:
            logger.debug('joke: ' + 'None')


@save_chatid
@strip_cmd
def direct_joke(bot, update):
    words = update.message.text
    logger.debug('words: ' + str(words))
    if len(words):
        answer = regex_joke(words) or random_joke(words) or 'Чо?'
    else:
        answer = 'Не нашел глагола'

    logger.debug('joke: ' + answer)
    update.message.reply_text(answer)


def bot_joke(bot, job):
    jq.run_once(bot_joke, get_next_start())
    for cid in CHATS:
        choose_bot_joke(cid, bot)


def choose_bot_joke(cid, bot):
    if rnd_percent(50):
        joke = dict_joke()
        logger.debug('joke: ' + joke)
        bot.send_message(chat_id=cid, text=joke)
    else:
        joke = sticker_id()
        logger.debug('joke: ' + joke)
        bot.send_sticker(chat_id=cid, sticker=joke)


updater = Updater(TOKEN)
jq = updater.job_queue

jq.run_once(bot_joke, get_next_start())
updater.dispatcher.add_handler(MessageHandler(Filters.text, joke))
updater.dispatcher.add_handler(CommandHandler('joke', direct_joke))

if POLL:
    updater.start_polling(poll_interval=POLL)
else:
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook(URL + TOKEN)

updater.idle()
