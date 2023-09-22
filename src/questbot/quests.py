import os
import logging

import yaml


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

    def process(self, filepath):
        """
        returns QuestDefinition object if processing is successfull
        and None if processing failed
        """

        obj = self._parse_yaml_file(filepath)

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
    """

    def __init__(self, name, description=""):
        self._name = ""
        self._description = ""
        self._start_date = ""
        self._duration = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value