import time
import logging
import threading
from datetime import datetime, timedelta

from questbot.events import QuestEvent, EventState
from questbot.definitions import QuestDefinition


logger = logging.getLogger(__name__)


class QuestController():
    """
    responsible for registering all configured quests
    and maintaining their statuses in relevant state
    """
    UPDATER_INTERVAL = 5
    REGISTRATION_DURATION = 30  # in minutes

    def __init__(self):
        self._quests = {}
        self._reg_delta = timedelta(minutes=self.REGISTRATION_DURATION)
        self._updater_active = True
        self._updater = threading.Thread(target=self.update)
        self._updater.start()

    def register(self, quest_definition):
        """
        registers QuestDefinition object for controller updates
        returns False if already registered
        returns True if newly registered
        """

        if quest_definition.name in self._quests:
            return False
        else:
            self._quests[quest_definition.name] = QuestEvent(quest_definition)
            return True

    def update(self):
        """
        updates the QuestDefinition objects to
        maintain their states (refer to EventState)
        """

        while self._updater_active:
            for qevent in self._quests.values():
                curstate = qevent.state
                curtime = datetime.now()

                if curtime < qevent.quest.start_date - self._reg_delta:
                    newstate = EventState.WAITING
                elif curtime < qevent.quest.start_date:
                    newstate = EventState.SCHEDULED
                elif curtime < qevent.quest.start_date + qevent.quest.duration:
                    newstate = EventState.RUNNING
                else:
                    newstate = EventState.FINISHED

                logger.debug(f"quest event ['{qevent.quest.name}'] has "
                             f"curstate={curstate.name} and newstate={newstate.name}")
                if curstate != newstate:
                    logger.info(f"quest event ['{qevent.quest.name}'] changed "
                                f"its state: {curstate.name} => {newstate.name}")
                qevent.state = newstate

            time.sleep(self.UPDATER_INTERVAL)

    def __del__(self):
        self._updater_active = False

