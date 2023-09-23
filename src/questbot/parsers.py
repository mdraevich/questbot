import os
import logging
from datetime import datetime, timedelta

import yaml
from pytimeparse.timeparse import timeparse
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from questbot.schemas import schemav1
from questbot.definitions import QuestDefinition, TeamDefinition, TaskDefinition


logger = logging.getLogger(__name__)


class QuestParser():
    """
    responsible for loading, parsing yaml files and
    returning QuestDefinition objects
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
