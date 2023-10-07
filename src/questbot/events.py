import logging
from enum import Enum

from questbot.users import User

logger = logging.getLogger(__name__)


class EventState(Enum):
    UNKNOWN = 1
    WAITING = 2
    SCHEDULED = 3
    RUNNING = 4
    FINISHED = 5


class QuestEvent():
    """
    represents quest definition with a state property and team controllers dict
    team controllers should be present if state is EventState.SCHEDULED or EventState.RUNNING
    """

    def __init__(self, quest_definition):
        self._quest_definition = quest_definition
        self._team_controllers = []
        self.state = EventState.UNKNOWN
        self._tc_generator = self._endless_team_controller_list()

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

    def register_team_controller(self, team_controller):
        """
        registers team controller for quest event
        """

        self._team_controllers.append(team_controller)

    def _endless_team_controller_list(self):
        """
        generator for endlessly iterating over registered team controllers
        """

        while True:
            for tc in self._team_controllers:
                yield tc

    def next_team_controller(self):
        """
        returns next registered team controller
        """

        return next(self._tc_generator)

    def get_team_controllers(self):
        """
        returns a list of registered team controllers
        """

        return self._team_controllers


class EventDistributor():
    """
    eventditributor is responsible for user notification
    user should subscribe to a eventditributor instance in order to
    receive events
    """

    def __init__(self):
        self._users = {}

    def subscribe(self, user):
        """
        subscribes user to events
        returns False if user already subscribed
        returns True if user newly subscribed
        """

        if not isinstance(user, User):
            raise ValueError("user must be an instance of <questbot.users.User> class")
        if user.user_id in self._users:
            return False

        logger.debug(f"user_id={user.user_id} has subscribed for events")
        self._users[user.user_id] = user
        return True

    def unsubscribe(self, user):
        """
        unsubscribes user to events
        returns False if user is not subscribed
        returns True if user is unsubscribed
        """

        if not isinstance(user, User):
            raise ValueError("user must be an instance of <questbot.users.User> class")
        if user.user_id not in self._users:
            return False

        logger.debug(f"user_id={user.user_id} has unsubscribed for events")
        self._users.pop(user.user_id)
        return True

    def notify(self, event):
        """
        sends to all subscribed users an arised event
        """

        for _, user in self._users.items():
            user.send_message(message=event)

    def clear(self):
        """
        unsubscribes all users from distribution
        """

        self._users = {}