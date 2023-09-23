import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


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