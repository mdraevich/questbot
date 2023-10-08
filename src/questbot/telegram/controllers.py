import os
import logging

import namesgenerator
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    CallbackQueryHandler,
    Filters,
    Dispatcher
)
from telegram import (
    ParseMode,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from questbot.users import User, UserState
from questbot.controllers import QuestController


logger = logging.getLogger(__name__)


class UserController():
    """
    responsible for actions asked by user
    using some bot commands
    """

    def __init__(self, dispatcher, quest_controller):
        self.controller = quest_controller
        self.dispatcher = dispatcher
        self._users = {}
        self._configure_routing()

    @property
    def dispatcher(self):
        return self._dispatcher

    @dispatcher.setter
    def dispatcher(self, value):
        if not isinstance(value, Dispatcher):
            raise ValueError("value must be an instance of "
                             "telegram.ext.Dispatcher")
        self._dispatcher = value

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, value):
        if not isinstance(value, QuestController):
            raise ValueError("value must be an instance of QuestController")
        self._controller = value

    def _configure_routing(self):
        routes = [
            CommandHandler("help", self.cmd_help),
            CommandHandler("start", self.cmd_start),
            CommandHandler("version", self.cmd_version)
        ]
        for route in routes:
            self.dispatcher.add_handler(route)

    def _register_new_user(self, user_id, chat_id, username):
        """
        returns an instance of User class by user_id
        if user_id is not in user database (self._users),
        then create a new User class and save it in user database
        """

        if user_id in self._users.keys():
            logger.info(f"User user_id={user_id}"
                         " is already registered")
        else:
            logger.info(f"User user_id={user_id} is now registered")
            user = User(user_id, chat_id, self.dispatcher)
            user.name = username or namesgenerator.get_random_name()
            self._users[user_id] = user

        self.controller.distributor.subscribe(self._users[user_id])
        return self._users[user_id]

    def cmd_help(self, update, context):
        pass

    def cmd_version(self, update, context):
        git_version = os.environ.get("GIT_VERSION") or "unknown-version"
        update.message.reply_text(git_version, parse_mode=ParseMode.HTML)

    def cmd_start(self, update, context):
        user_id = update.message.from_user["id"]
        chat_id = update.message.chat_id
        username = update.message.from_user["username"]

        user = self._register_new_user(user_id, chat_id, username)
        update.message.reply_text(f"Hello, {user.name}!",
                                  parse_mode=ParseMode.HTML)

    def cmd_register(self, update, context):
        pass

    def cmd_unregister(self, update, context):
        pass

    def cmd_about_team(self, update, context):
        pass

    def cmd_about_me(self, update, context):
        pass

    def cmd_get_hint(self, update, context):
        pass

    def cmd_give_answer(self, update, context):
        pass