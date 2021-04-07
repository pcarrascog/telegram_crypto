#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import os
import requests
from requests.exceptions import HTTPError

import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Error(Exception):
    pass

class NotAdmitedError(Error):
    pass


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    logger
    update.message.reply_text('Hi! :)')


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def btc_command(update: Update, _: CallbackContext) -> None:
    try:
        market_id = 'btc-clp'
        url = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'
        response = requests.get(url)
        #print(response.json())
        jsonResponse = response.json()
        update.message.reply_text(jsonResponse["ticker"]["last_price"])
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

def ltc_command(update: Update, _: CallbackContext) -> None:
    try:
        market_id = 'ltc-clp'
        url = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'
        response = requests.get(url)
        #print(response.json())
        jsonResponse = response.json()
        update.message.reply_text(jsonResponse["ticker"]["last_price"])
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


def budda_command(update: Update, callback: CallbackContext) -> None:
    budda_coins = ('btc', 'eth', 'ltc', 'bch')
    try:
        market_id = context.args[0]
        if market_id in budda_coins:
            market_id = market_id + '-clp'
        else:
            raise NotAdmitedError
        url = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'
        response = requests.get(url)
        #print(response.json())
        jsonResponse = response.json()
        update.message.reply_text(jsonResponse["ticker"]["last_price"])
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    except NotAdmitedError:
        print(f'This coin is not admited')
        print()


def inlinequery(update: Update, _: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query == "":
        return

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Bold",
            input_message_content=InputTextMessageContent(
                f"*{escape_markdown(query)}*", parse_mode=ParseMode.MARKDOWN
            ),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="Italic",
            input_message_content=InputTextMessageContent(
                f"_{escape_markdown(query)}_", parse_mode=ParseMode.MARKDOWN
            ),
        ),
    ]

    update.inline_query.answer(results)


def main() -> None:
    # Create the Updater and pass it your bot's token.
    TOKEN = os.getenv('TOKEN')
    print(TOKEN)
    updater = Updater(TOKEN, use_context=True)  # use_context by default True

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("btc", btc_command))
    dispatcher.add_handler(CommandHandler("ltc", ltc_command))
    dispatcher.add_handler(CommandHandler("budda", budda_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
