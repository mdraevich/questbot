import time
import logging
import threading
from datetime import datetime, timedelta

from questbot.events import (
    QuestEvent,
    EventState,
    EventDistributor,
    EventIdMapper
)
from questbot.definitions import QuestDefinition, TeamDefinition

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
        self._distributor = EventDistributor()
        self._event_mapper = EventIdMapper()
        self._reg_delta = timedelta(minutes=self.REGISTRATION_DURATION)

        # separate thread for quest state updates
        self._updater_active = True
        self._updater = threading.Thread(target=self.update)
        self._updater.start()

    @property
    def distributor(self):
        return self._distributor

    def register(self, quest_definition):
        """
        registers QuestDefinition object for controller updates
        returns False if already registered
        returns True if newly registered
        """

        if not isinstance(quest_definition, QuestDefinition):
            raise ValueError("quest_definition must be an instance of "
                             "QuestDefinition class")

        if quest_definition.name in self._quests:
            return False

        qevent = QuestEvent(quest_definition)
        for team_definition in quest_definition.get_teams():
            qevent.register_team_controller(TeamController(team_definition))
            logger.debug(f"Registered a new team controller with "
                         f"team_definition.name='{team_definition.name}' "
                         f"for qevent.quest.name='{qevent.quest.name}'")

        self._quests[quest_definition.name] = qevent
        return True

    def join_quest(self, user, qevent_id):
        """
        returns True if user has been successfully registered for a quest event
        returns False if user failed to be registered for a quest event
        """

        try:
            qevent = self._event_mapper.get_event(qevent_id)
        except KeyError:
            logger.debug(f"Cannot find qevent_id={qevent_id} in EventIdMapper")
            return False

        try:
            team_controller = qevent.next_team_controller()
            team_controller.distributor.subscribe(user)
            user.set_team_controller(team_controller)
        except ValueError:
            logger.exception("Cannot subscribe user to TeamController.Distributor")
            return False

        return True

    def run_quest(self, qevent):
        """
        runs a quest by calling start() in every
        registered team controller in QuestEvent
        """

        for tc in qevent.get_team_controllers():
            tc.start()

    def process_change(self, qevent, newstate):
        if newstate == EventState.SCHEDULED:
            qevent_id = self._event_mapper.register_event(qevent)
            qevent.annotations["qevent_id"] = qevent_id
            logger.info("QuestEvent instance is now registered in EventIdMapper "
                        f"with qevent_id={qevent_id}")
            self.distributor.notify_template(
                "quest_scheduled",
                qevent_id=qevent_id,
                date=qevent.quest.start_date,
                duration=qevent.quest.duration,
                quest_name=qevent.quest.name,
                quest_description=qevent.quest.description,
                teams="\n".join([ f"▫️{team.name}"
                                  for team in qevent.quest.get_teams() ]))

        elif newstate == EventState.RUNNING:
            qevent_id = qevent.annotations.get("qevent_id", "")
            if self._event_mapper.remove_event(qevent_id):
                qevent.annotations.pop(qevent_id)
                logger.info("QuestEvent instance is now removed from "
                            f"EventIdMapper by qevent_id={qevent_id}")

            self.run_quest(qevent)

        elif newstate == EventState.FINISHED:
            qevent_id = qevent.annotations.get("qevent_id", "")
            if self._event_mapper.remove_event(qevent_id):
                qevent.annotations.pop(qevent_id)
                logger.info("QuestEvent instance is now removed from "
                            f"EventIdMapper by qevent_id={qevent_id}")

            self.distributor.notify("Quest is finished!")

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
                    self.process_change(qevent, newstate)
                qevent.state = newstate

            time.sleep(self.UPDATER_INTERVAL)

    def __del__(self):
        self._updater_active = False


class TeamController():
    """
    responsible for interacting with a team
    in accordance to team definition
    """

    def __init__(self, team_definition):
        self.team = team_definition
        self._distributor = EventDistributor()

    @property
    def team(self):
        return self._team

    @team.setter
    def team(self, value):
        if not isinstance(value, TeamDefinition):
            raise ValueError("value must be an instance of "
                             "TeamDefinition class")
        self._team = value

    @property
    def distributor(self):
        return self._distributor

    def give_hint(self):
        """
        returns True if hint is available
        returns False if there're no hints
        """

        if len(self.current_hints):
            hint_value = self.current_hints.pop(0)
            logger.info(f"Team team_definition.name='{self.team.name}' "
                        f"has requested a hint ({len(self.current_hints)} "
                        f"more available) for task={self.current_task + 1}")

            self.distributor.notify("Your team member has requested a hint!")
            self.distributor.notify(hint_value)
            return True
        else:
            logger.info(f"Team team_definition.name='{self.team.name}' "
                        f"has requested a hint, but there're no avaiable hints "
                        f"for task={self.current_task + 1}")
            self.distributor.notify("Your team member has requested a hint, "
                                    "but there're no avaiable ones :c")
            return False

    def check_answer(self, value):
        """
        return True if answer is right
        return False if answer is wrong
        """

        correct_value = self.team.get_tasks()[self.current_task].answer
        if value.lower() == correct_value.lower():
            logger.info(f"Team team_definition.name='{self.team.name}' "
                        f"has given a correct answer='{value}' "
                        f"to task={self.current_task + 1}")
            self.distributor.notify("Your team member has sent a correct answer!")
            self.next_task()
            return True
        else:
            logger.info(f"Team team_definition.name='{self.team.get_tasks()}' "
                        f"has given a wrong answer='{value}' "
                        f"to task={self.current_task + 1}")
            self.distributor.notify("Your team member has sent a wrong answer!")
            return False

    def next_task(self):
        """
        assignes a new task to a team
        returns True if a new task available
        returns False if no tasks are available
        """

        self.current_task += 1
        if self.current_task == len(self.team.get_tasks()):
            logger.info(f"Team team_definition.name='{self.team.name}' "
                         "has completed all available tasks")
            self.distributor.notify("Team, I have no questions for you :c")
            return False
        else:
            logger.info(f"Team team_definition.name='{self.team.name}' "
                        f"has started task={self.current_task + 1}")
            self.distributor.notify("Team, be ready for new question!")
            self.current_hints = self.team.get_tasks()[self.current_task].get_hints()
            return True

    def start(self):
        """
        starts giving tasks for team
        """

        logger.info(f"Team team_definition.name='{self.team.name}' "
                    f"has started the quest")
        self.distributor.notify("Team, be ready, we will begin NOW!")
        self.current_hints = []
        self.current_task = -1
        self.next_task()

    def stop(self):
        """
        stops giving tasks for team
        clears all subscribed users
        """

        logger.info(f"Team team_definition.name='{self.team.name}' "
                    f"has finished the quest")
        self.distributor.notify("Team, nice game, it's finished NOW!")
        self.distributor.clear()
