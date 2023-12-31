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
from telegram.ext import Updater

from questbot.parsers import QuestParser
from questbot.controllers import QuestController
from questbot.users import User
from questbot.telegram.controllers import UserController


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.getLevelName(os.environ.get("LOGLEVEL") or "WARNING")
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    bot_api_key = os.environ.get("BOT_API_KEY", None)
    storage_path = os.environ.get("STORAGE_PATH", "./data.pkl")
    if bot_api_key is None:
        logger.error("specify BOT_API_KEY variable")
        sys.exit(1)

    parser = QuestParser()
    quest_controller = QuestController()
    quests = [parser.process(item) for item in parser.list('./quests')]
    is_registered = all([quest_controller.register(quest) for quest in quests])
    if not is_registered:
        logger.warning("Duplicated quest names are found, be sure "
                       "quest configs have no errors and duplicates.")

    updater = Updater(bot_api_key)
    dispatcher = updater.dispatcher
    
    user_controller = UserController(dispatcher, quest_controller, storage_path)    
    updater.start_polling()
    updater.idle()