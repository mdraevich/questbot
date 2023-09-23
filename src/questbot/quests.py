import os
import time
import logging
import threading
from datetime import datetime, timedelta

import yaml
from pytimeparse.timeparse import timeparse
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from questbot.schemas import schemav1
from questbot.ext import EventState


logger = logging.getLogger(__name__)


class QuestController():
    """
    responsible for registering all configured quests
    and maintaining their statuses in relevant state
    """
    UPDATER_INTERVAL = 2

    def __init__(self):
        self._quests = {}
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
        maintain their states (refer to QuestEvent.STATES)
        """

        while self._updater_active:
            for qevent in self._quests.values():
                curstate = qevent.state
                curtime = datetime.now()

                if curtime < qevent.quest.start_date - timedelta(minutes=30):
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


class QuestParser():
    """
    """

    def __init__(self):
        pass

    def _parse_yaml_file(self, filepath):
        """
        parses yaml file and returns object
        """

        try:
            with open(filepath, "r") as file:
                return yaml.safe_load(file)
        except (yaml.YAMLError, OSError) as exc:
            if isinstance(exc, OSError):
                print("Cannot read configuration file, "
                      "check path and permissions")
            if isinstance(exc, yaml.YAMLError):
                print("Config file has incorrect format, "
                      "cannot parse config options")
            return None

    def _validate_definition(self, definition):
        try:
            validate(instance=definition, schema=schemav1)
            return True
        except ValidationError:
            return False

    def process(self, filepath):
        """
        returns QuestDefinition object if processing is successfull
        and None if processing failed
        """

        obj = self._parse_yaml_file(filepath)
        if not self._validate_definition(obj):
            logger.error("ValidationError: validation failed "
                         "for quest definition")
            return None

        quest = QuestDefinition()
        quest.name, quest.description = obj["name"], obj["description"]
        quest.duration = timedelta(seconds=timeparse(obj["duration"]))
        quest.start_date = datetime.fromisoformat(obj["start_date"])

        for team_obj in obj["teams"]:
            team = TeamDefinition()
            team.name = team_obj["name"]
            team.description = team_obj["description"]
            team.communication = team_obj["communication"]
            for task_obj in team_obj["tasks"]:
                task = TaskDefinition()
                task.question = task_obj["question"]
                task.answer = task_obj["answer"]
                for hint in task_obj["hints"]:
                    task.add_hint(hint)
                team.add_task(task)
            quest.add_team(team)

        return quest

    def list(self, directory):
        """
        returns list of yml/yaml files
        in the specified directory

        can be used to list all quest file definitions
        """

        files = []
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if (os.path.isfile(filepath) and filepath.endswith('.yml')
                or filepath.endswith('.yaml')):
                files.append(filepath)
        return files


class QuestDefinition():
    """
    name         - str, quest name 
    description  - str, quest description
    start_date   - datetime, quest start date & time
    duration     - timedelta, quest duration 
    """

    def __init__(self):
        self._name = ""
        self._description = ""
        self._start_date = datetime.now()
        self._duration = timedelta(minutes=30)
        self._teams = []

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def start_date(self):
        return self._start_date

    @property
    def duration(self):
        return self._duration

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("name must be string")
        self._name = value

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("description must be string")
        self._description = value

    @start_date.setter
    def start_date(self, value):
        if not isinstance(value, datetime):
            raise ValueError("start_date must be datetime.datetime")
        self._start_date = value

    @duration.setter
    def duration(self, value):
        if not isinstance(value, timedelta):
            raise ValueError("duration must be datetime.timedelta")
        self._duration = value

    def add_team(self, team_definition):
        if not isinstance(team_definition, TeamDefinition):
            raise ValueError("team_definition must be an instance of "
                             "TeamDefinition class")
        self._teams.append(team_definition)

    def get_teams(self):
        return self._teams[:]


class TeamDefinition():
    """
    class to represent team definition
    """

    def __init__(self):
        self._name = ""
        self._description = ""
        self._communication = ""
        self._tasks = []

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def communication(self):
        return self._communication

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("name must be string")
        self._name = value

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise ValueError("description must be string")
        self._description = value

    @communication.setter
    def communication(self, value):
        if not isinstance(value, str):
            raise ValueError("communication must be string")
        self._communication = value

    def add_task(self, task_definition):
        if not isinstance(task_definition, TaskDefinition):
            raise ValueError("task_definition must be an instance"
                             "of TaskDefinition class")
        self._tasks.append(task_definition)

    def get_tasks(self):
        return self._tasks[:]


class TaskDefinition():
    """
    class to represent task definition
    that's used in team definition class
    """

    def __init__(self):
        self._question = ""
        self._answer = ""
        self._hints = []

    @property
    def question(self):
        return self._question

    @property
    def answer(self):
        return self._answer

    @question.setter
    def question(self, value):
        if not isinstance(value, str):
            raise ValueError("question must be string")
        self._question = value

    @answer.setter
    def answer(self, value):
        if not isinstance(value, str):
            raise ValueError("answer must be string")
        self._answer = value

    def add_hint(self, hint):
        if not isinstance(hint, str):
            raise ValueError("hint must be string")
        self._hints.append(hint)

    def get_hints(self):
        return self._hints[:]