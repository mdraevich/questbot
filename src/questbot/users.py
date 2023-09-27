import logging
from enum import Enum


logger = logging.getLogger(__name__)


class UserState(Enum):
    IDLE = 1
    REGISTERED = 2
    PLAYING = 3
    DELETED = 4


class User():
    """
    represents a general user account
    """

    def __init__(self, user_id, chat_id, dispatcher):
        self._name = ""
        self._user_id = user_id
        self._chat_id = chat_id
        self._dispatcher = dispatcher
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
    def state(self):
        return self._state

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("name must be string")
        self._name = value

    @state.setter
    def state(self, value):
        if not isinstance(value, UserState):
            raise ValueError("state must be an instance of UserState")
        self._state = value

    def send_message(self, message):
        self._dispatcher.bot.sendMessage(chat_id=self.chat_id, text=message)
