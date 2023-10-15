import logging
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class EfficiencyController:
    """
    controls the result for a team to rate its efficiency
    """

    def __init__(self):
        self._tasks = []

    def new_task(self):
        """
        registers a new task as a current task
        """
        self._penalty_counter = 0
        self._start_date = datetime.now()

        pass

    def finish_task(self):
        """
        finishes a current task
        """

        self._tasks.append(EfficiencyItem(datetime.now() - self._start_date,
                                          self._penalty_counter))

    def add_penalty(self, value):
        """
        adds penalty for a current task
        """

        self._penalty_counter += value

    def appraise(self):
        """
        appraise each element in self._tasks
        returns list of lists
        """

        return [item.appraise() for item in self._tasks]

    def appraise_total(self):
        """
        appraise each element in self._tasks
        returns int - total sum of appraise numbers
        """

        return sum([sum(item.appraise()) for item in self._tasks])


class EfficiencyItem():
    """
    defines an item for calculating the result efficiency
    """
    PENALTY_VALUE = 250  # penalty per hint
    DURATION_MAX_VALUE = timedelta(minutes=30)

    TIME_BONUS = 2000
    NO_PENALTY_BONUS = 2000
    COMPLETED_BONUS = 1000

    def __init__(self, duration, penalty):
        self.duration = duration
        self.penalty = penalty

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, timedelta):
            raise ValueError("value must be an instance "
                             "of type 'datetime.timedelta'")
        self._duration = value

    @property
    def penalty(self):
        return self._penalty

    @penalty.setter
    def penalty(self, value):
        if not isinstance(value, int):
            raise ValueError("value must be an instance "
                             "of type 'int'")
        if value < 0:
            raise ValueError("value must be an integer value >= 0")

        self._penalty = value

    def appraise(self):
        """
        calculates the points for the task item
        """

        return [
            self.COMPLETED_BONUS,
            max(0, self.NO_PENALTY_BONUS - self._penalty * self.PENALTY_VALUE),
            max(0, self.TIME_BONUS - int(self.TIME_BONUS
                                  * self.duration.total_seconds()
                                  / self.DURATION_MAX_VALUE.total_seconds()))
        ]