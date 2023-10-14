import os
import re
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
from questbot.controllers import QuestController, TeamController
from questbot.telegram.answers import BotTemplates

logger = logging.getLogger(__name__)


class UserController():
    """
    responsible for actions asked by user
    using some bot commands
    """

    def __init__(self, dispatcher, quest_controller):
        self.controller = quest_controller
        self.dispatcher = dispatcher
        self._bot = BotTemplates()
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
            CommandHandler("version", self.cmd_version),
            CommandHandler("nickname", self.cmd_change_nickname),
            CommandHandler("register", self.cmd_register),
            CommandHandler("unregister", self.cmd_unregister),
            CommandHandler("answer", self.cmd_give_answer),
            CommandHandler("hint", self.cmd_get_hint),
            CommandHandler("help", self.cmd_help)
        ]
        for route in routes:
            self.dispatcher.add_handler(route)

    def _register_new_user(self, user_id, chat_id, first_name, last_name):
        """
        returns True if user is registered successfully
        returns False if user is already registered
        """

        if user_id in self._users.keys():
            logger.info(f"User user_id={user_id}"
                         " is already registered")
            return False
        else:
            logger.info(f"User user_id={user_id} is now registered")
            user = User(user_id, chat_id, self.dispatcher)
            user.name = f"{first_name} {last_name}".strip()
            self._users[user_id] = user
            return True

    def _get_user(self, user_id):
        """
        returns an instance of User class by user_id 
            from user database (self._users)
        
        returns None if no user exists for specified user_id
        """

        return self._users.get(user_id, None)

    def _validate_nickname(self, nickname):
        return re.fullmatch('[\\w]{3,25}', nickname)

    def _validate_answer(self, value):
        return re.fullmatch('[\\w]{1,25}', value)

    def _validate_qevent_id(self, qevent_id):
        return re.fullmatch('[\\d]{4}', qevent_id)

    def cmd_help(self, update, context):
        lang_code = str(update.message.from_user.language_code)
        answer_tmpl = self._bot.get_answer_template("help", lang_code)
        answer = answer_tmpl.substitute()
        update.message.reply_text(answer, parse_mode=ParseMode.HTML)

    def cmd_version(self, update, context):
        git_version = os.environ.get("GIT_VERSION") or "unknown-version"
        update.message.reply_text(git_version, parse_mode=ParseMode.HTML)

    def cmd_start(self, update, context):
        lang_code = str(update.message.from_user.language_code)
        answer_tmpl = self._bot.get_answer_template("hello", lang_code)

        user_id = update.message.from_user["id"]
        chat_id = update.message.chat_id
        first_name = update.message.from_user["first_name"] or " "
        last_name = update.message.from_user["last_name"] or " "

        self._register_new_user(user_id, chat_id, first_name, last_name)
        self._get_user(user_id).lang_code = lang_code
        self.controller.distributor.subscribe(self._get_user(user_id))

        answer = answer_tmpl.substitute(name=self._get_user(user_id).name)
        update.message.reply_text(answer, parse_mode=ParseMode.HTML)

    def cmd_register(self, update, context):
        lang_code = str(update.message.from_user.language_code)
        user_id = update.message.from_user["id"]
        user = self._get_user(user_id)
        if user is None:
            raise KeyError(f"No user is found for user_id={user_id}")

        qevent_id = " ".join(context.args)
        answer_tmpl = self._bot.get_answer_template(
                                        "register_qevent_fail", lang_code)
        if self._validate_qevent_id(qevent_id):
            if self.controller.join_quest(user, qevent_id):
                answer_tmpl = self._bot.get_answer_template(
                                        "register_qevent_success", lang_code)

        answer = answer_tmpl.substitute(qevent_id=qevent_id)
        update.message.reply_text(answer, parse_mode=ParseMode.HTML)

    def cmd_unregister(self, update, context):
        lang_code = str(update.message.from_user.language_code)
        user_id = update.message.from_user["id"]
        user = self._get_user(user_id)
        if user is None:
            raise KeyError(f"No user is found for user_id={user_id}")

        template_name = "unregister_fail"
        if self.controller.leave_quest(user):
            template_name = "unregister_success"

        answer_tmpl = self._bot.get_answer_template(template_name, lang_code)
        answer = answer_tmpl.substitute()
        update.message.reply_text(answer, parse_mode=ParseMode.HTML)

    def cmd_about_team(self, update, context):
        pass

    def cmd_about_me(self, update, context):
        pass

    def cmd_get_hint(self, update, context):
        lang_code = str(update.message.from_user.language_code)
        user_id = update.message.from_user["id"]
        user = self._get_user(user_id)
        if user is None:
            raise KeyError(f"No user is found for user_id={user_id}")

        if user.state != UserState.PLAYING:
            template_name = "get_hint_fail"
            answer_tmpl = self._bot.get_answer_template(template_name, lang_code)
            answer = answer_tmpl.substitute()
            update.message.reply_text(answer, parse_mode=ParseMode.HTML)
        else:
            team_controller = user.get_team_controller()
            assert isinstance(team_controller, TeamController), \
                    (f"User user_id={user_id} has incorrect team_controller "
                     f"of class '{type(team_controller)}'")
            team_controller.give_hint(user)

    def cmd_give_answer(self, update, context):
        lang_code = str(update.message.from_user.language_code)
        user_id = update.message.from_user["id"]
        user = self._get_user(user_id)
        if user is None:
            raise KeyError(f"No user is found for user_id={user_id}")

        user_answer = " ".join(context.args)
        if user.state != UserState.PLAYING:
            template_name = "give_answer_fail"
        elif not self._validate_answer(user_answer):
            template_name = "give_answer_wrong_format"
        else:
            team_controller = user.get_team_controller()
            assert isinstance(team_controller, TeamController), \
                    (f"User user_id={user_id} has incorrect team_controller "
                     f"of class '{type(team_controller)}'")

            team_controller.check_answer(user, user_answer)
            return

        answer_tmpl = self._bot.get_answer_template(template_name, lang_code)
        answer = answer_tmpl.substitute()
        update.message.reply_text(answer, parse_mode=ParseMode.HTML)


    def cmd_change_nickname(self, update, context):
        lang_code = str(update.message.from_user.language_code)

        user_id = update.message.from_user["id"]
        user = self._get_user(user_id)
        if user is None:
            raise KeyError(f"No user is found for user_id={user_id}")
            
        new_nickname = " ".join(context.args)
        if self._validate_nickname(new_nickname):
            user.name = new_nickname
            answer_tmpl = self._bot.get_answer_template("change_nickname_success",
                                                    lang_code)
            answer = answer_tmpl.substitute()
            update.message.reply_text(answer, parse_mode=ParseMode.HTML)
        else:
            logger.warning(f"User user_id={user_id} has supplied "
                           "an invalid nickname")
            answer_tmpl = self._bot.get_answer_template("change_nickname_fail",
                                                    lang_code)
            answer = answer_tmpl.substitute()
            update.message.reply_text(answer, parse_mode=ParseMode.HTML)