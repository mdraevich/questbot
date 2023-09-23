import logging
from enum import Enum


logger = logging.getLogger(__name__)


class EventState(Enum):
    UNKNOWN = 1
    WAITING = 2
    SCHEDULED = 3
    RUNNING = 4
    FINISHED = 5


class QuestEvent():
    """
    represents quest definition with a state property
    """

    def __init__(self, quest_definition):
        self._quest_definition = quest_definition
        self.state = EventState.UNKNOWN

    @property
    def state(self):
        return self._state

    @property
    def quest(self):
        return self._quest_definition

    @state.setter
    def state(self, value):
        if not isinstance(value, EventState):
            raise ValueError(f"state must be a value from list {list(EventState)}")
        self._state = value
