from abc import abstractmethod
from api.loghandler.log import Log


class LogHandler:
    @abstractmethod
    def handle(self, log: Log):
        pass