import os
import logging
from datetime import datetime, timedelta

import yaml
from pytimeparse.timeparse import timeparse
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from questbot.schemas import schemav1


logger = logging.getLogger(__name__)


class QuestController():
    """
    responsible for registering all configured quests
    and maintaining their statuses in relevant state
    """

    def __init__(self):
        pass

    def register(self, question_definition):
        """
        registers QuestionDefinition object and starts
        controlling its state
        """

        pass

    def update(self):
        """
        updates the QuestionDefinition objects to
        maintain their states (waiting, scheduled, running, finished)
        """

        pass


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
        definition = QuestDefinition()
        logger.debug(self._validate_definition(obj))

        delta = timedelta(seconds=timeparse(obj["duration"]))
        timedate = datetime.fromisoformat(obj["start_date"])

        logger.debug(timedate)
        logger.debug(timedate + delta)
        return None

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
        self._name = value

    @description.setter
    def description(self, value):
        self._description = value

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @duration.setter
    def duration(self, value):
        self._duration = value

    def create_team(self):
        pass


class TeamDefinition():
    """
    """

    def __init__(self):
        pass