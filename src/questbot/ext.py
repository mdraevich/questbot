from enum import Enum


class EventState(Enum):
    UNKNOWN = 1
    WAITING = 2
    SCHEDULED = 3
    RUNNING = 4
    FINISHED = 5
