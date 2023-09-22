import os
import sys
import time
import json
import random
import logging

import yaml
from urllib import request, error
from difflib import SequenceMatcher

from jinja2 import Environment, BaseLoader
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    CallbackQueryHandler,
    Filters
)
from telegram import (
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from questbot.quests import QuestDefinition


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.getLevelName(os.environ.get("LOGLEVEL") or "WARNING")
)
logger = logging.getLogger(__name__)


def show_version_info(update, context):
    git_version = os.environ.get("GIT_VERSION") or "unknown-version"
    update.message.reply_text(git_version, parse_mode=ParseMode.HTML)     


if __name__ == "__main__":
    bot_api_key = os.environ.get("BOT_API_KEY", None)
    if bot_api_key is None:
        print("specify BOT_API_KEY variable")
        sys.exit(1)

    updater = Updater(bot_api_key)
    dispatcher = updater.dispatcher
    
    # dispatcher.add_handler(CommandHandler("start", show_version_info))
    # dispatcher.add_handler(CommandHandler("help", help_handler))
    dispatcher.add_handler(CommandHandler("version", show_version_info))
    
    updater.start_polling()
    updater.idle()