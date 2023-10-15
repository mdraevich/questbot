import logging
from enum import Enum

from telegram import ParseMode

logger = logging.getLogger(__name__)


class UserState(Enum):
    IDLE = 1
    PLAYING = 2
    DELETED = 3


class User():
    """
    represents a general user account
    """

    def __init__(self, user_id, chat_id, dispatcher):
        self._name = ""
        self._lang_code = ""
        self._user_id = user_id
        self._chat_id = chat_id
        self._dispatcher = dispatcher
        self._team_controller = None
        self.state = UserState.IDLE

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._user_id

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def lang_code(self):
        return self._lang_code

    @property
    def state(self):
        return self._state

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("name must be string")
        self._name = value

    @lang_code.setter
    def lang_code(self, value):
        if not isinstance(value, str):
            raise ValueError("value must be string")
        self._lang_code = value

    @state.setter
    def state(self, value):
        if not isinstance(value, UserState):
            raise ValueError("state must be an instance of UserState")
        self._state = value

    def send_message(self, message):
        if self.state == UserState.DELETED:
            logger.error(f"User user_id={self.user_id} and "
                         f"username={self.username} is already deleted, but "
                         "trying to send message to it")
        else:
            self._dispatcher.bot.sendMessage(chat_id=self.chat_id,
                                             text=message,
                                             parse_mode=ParseMode.HTML)

    def set_team_controller(self, team_controller):
        """
        sets team controller and state to UserState.PLAYING
        """

        self._team_controller = team_controller
        self.state = UserState.PLAYING

    def get_team_controller(self):
        """
        returns team controller instance
        """

        return self._team_controller

    def remove_team_controller(self):
        """
        sets team controller to None and changes user state to UserState.IDLE
        returns True if a team controller is set
        returns False if a team controller is already None
        """

        if self.state == UserState.DELETED:
            logger.error(f"User user_id={self.user_id} and "
                         f"username={self.username} is already deleted, but "
                         "trying to remove team controller for it")
        else:
            is_playing = self._team_controller is not None
            self.state = UserState.IDLE
            self._team_controller = None
            return is_playing
