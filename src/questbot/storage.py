import pickle
import logging


logger = logging.getLogger(__name__)


class DataStorage:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'wb') as file:
            pickle.dump(data, file)

    def load(self):
        try:
            with open(self.filename, 'rb') as file:
                data = pickle.load(file)
                return data
        except FileNotFoundError:
            logger.error(f"File '{self.filename}' not found.")
            return None
        except Exception as e:
            logger.error(f"An error occurred while loading the data: {str(e)}")
            return None
