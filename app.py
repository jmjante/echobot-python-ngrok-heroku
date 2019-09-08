#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tgbot.config import mode, bot_token, bot_user_name, HEROKU_APP_NAME, NGROK_APP_NAME

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

# mode = os.getenv("MODE")
MODE = mode
TOKEN = bot_token

if MODE == "dev":
    PORT = "80"
    DOMAIN = ".ngrok.io/"
    APP_NAME = NGROK_APP_NAME

elif MODE == "prod":
    # PORT = "8443"
    PORT = int(os.environ.get("PORT", "8443"))
    DOMAIN = ".herokuapp.com/"
    APP_NAME = HEROKU_APP_NAME

else:
    logger.error("No MODE specified!")
    sys.exit(1)


def run(updater):
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    s = updater.bot.set_webhook("https://{}{}{}".format(APP_NAME,DOMAIN,TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"


def start(update, context):
    update.message.reply_text('Hi!')


def help(update, context):
    update.message.reply_text('Help!')


def echo(update, context):
    update.message.reply_text(update.message.text)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    # Start the Bot
    run(updater)
    updater.idle()

if __name__ == '__main__':
    main()