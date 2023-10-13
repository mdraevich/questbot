import random
import logging
from enum import Enum

from questbot.users import User
from questbot.telegram.answers import BotTemplates


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
        self.annotations = {}
        self.state = EventState.UNKNOWN
        self._tc_generator = self._endless_team_controller_list()

    @property
    def annotations(self):
        return self._annotations

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

    @annotations.setter
    def annotations(self, value):
        if not isinstance(value, dict):
            raise ValueError(f"value must be a type of 'dict'")
        self._annotations = value

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
        self._bot = BotTemplates()

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

    def notify_template(self, template_name, **kwargs):
        """
        sends to all subscribed users an arised event
        """

        for _, user in self._users.items():
            answer_tmpl = self._bot.get_answer_template(template_name,
                                                        user.lang_code)
            answer = answer_tmpl.substitute(**kwargs)
            user.send_message(message=answer)

    def clear(self):
        """
        unsubscribes all users from distribution
        """

        self._users = {}


class EventIdMapper():
    """
    class is responsible for registering & reading events by its id

    NOTE:
    qevent identifier is <ID_LENGTH>-digit number,
    so total number of events to be registered is limited
    """
    MAX_RANDOM_CYCLES = 10
    ID_LENGTH = 4

    def __init__(self):
        self._qevents = {}

    def _generate_random_id(self):
        """
        generates random string id and returns it
        """

        short_id = str(random.randint(0, 10000))
        full_id = "0" * (self.ID_LENGTH - len(short_id)) + short_id
        return full_id

    def register_event(self, qevent):
        """
        registers qevent in local db and returns its identifier
        """
        
        is_success = False
        for i in range(self.MAX_RANDOM_CYCLES):
            free_id = self._generate_random_id()
            if free_id not in self._qevents.keys():
                is_success = True
                break

        assert is_success, "Cannot generate unique identifier for qevent"
        assert isinstance(free_id, str), ("Generated identifier is not "
                                          "a type of 'str'")
        assert len(free_id) == self.ID_LENGTH, ("Generated identifier has "
                                                "incorrect length "
                                                f"{len(free_id)} != {self.ID_LENGTH}")
        self._qevents[free_id] = qevent
        return free_id

    def get_event(self, qevent_id):
        """
        returns qevent from local db by identifier
        raise exception KeyError if qevent_id not found
        """

        if qevent_id not in self._qevents.keys():
            raise KeyError(f"Cannot find qevent_id={qevent_id} in local database")

        return self._qevents[qevent_id]

    def remove_event(self, qevent_id):
        """
        returns True if it has removed the element
        returns False if it no qevent_id was found in local db
        """

        if qevent_id not in self._qevents.keys():
            return False
        else:
            self._qevents.pop(qevent_id)
            return True