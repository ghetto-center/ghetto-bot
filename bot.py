#! /usr/bin/env python3

import logging

import pymorphy2
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from app.app_config import config
from joke import random_joke, regex_joke, dict_joke, sticker_id, reply_sticker_id, random_dumb_joke, random_mom_joke
from joke_utils import get_next_start, rnd_percent

logger = logging.getLogger(__name__)

morph = pymorphy2.MorphAnalyzer()

TOKEN = config.get('TOKEN')
PORT = config.get('PORT')


def save_chat_id(func):
    def wrap(*args, **kwargs):
        # magic
        args[0].CHATS.add(args[2].message.chat_id)
        func(*args, **kwargs)

    return wrap


class GhettoBotUpdater(Updater):
    CHATS = set([])

    def choose_bot_joke(self, cid):
        if rnd_percent(50):
            joke = dict_joke()
            logger.debug('joke: ' + joke)
            self.bot.send_message(chat_id=cid, text=joke)
        else:
            joke = sticker_id()
            logger.debug('joke: ' + joke)
            self.bot.send_sticker(chat_id=cid, sticker=joke)

    def bot_joke(self, bot, job):
        # recurse loop
        self.job_queue.run_once(self.bot_joke, get_next_start())

        for cid in self.CHATS:
            self.choose_bot_joke(cid)

    @save_chat_id
    def direct_joke(self, bot, update, **optional_args):
        words = ' '.join(optional_args.get('args', []))
        logger.debug('words: ' + str(words))
        if len(words):
            answer = regex_joke(words) or random_joke(words) or 'отъебись'
        elif rnd_percent(30):
            answer = random_dumb_joke()
        else:
            answer = random_mom_joke()

        logger.debug('joke: ' + answer)
        update.message.reply_text(answer)

    @save_chat_id
    def joke(self, bot, update, **optional_args):
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

    def _add_handler(self, handler):
        self.dispatcher.add_handler(handler)

    def add_command_handler(self, command, callback, pass_args=False):
        self._add_handler(CommandHandler(command, callback, Filters.command, pass_args=pass_args))

    def add_message_handler(self, callback, pass_user_data=False):
        self._add_handler(MessageHandler(Filters.text, callback, pass_user_data=pass_user_data))

    def start_ghetto_bot(self):
        self.job_queue.run_once(self.bot_joke, get_next_start())

        self.add_message_handler(self.joke, pass_user_data=True)
        self.add_command_handler('joke', self.direct_joke, pass_args=True)

        self.start_polling()
        self.start_webhook(port=PORT)
        self.idle()


def start():
    GhettoBotUpdater(token=TOKEN, workers=10).start_ghetto_bot()


if __name__ == '__main__':
    start()
