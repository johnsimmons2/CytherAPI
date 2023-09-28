from datetime import datetime
from enum import Enum


class Log:
    def __init__(self, lvl, msg, ref = None, err = None, time = None):
        super().__init__()
        self.timestamp = datetime.now() if time is None else time
        self.lvl = lvl
        self.msg = msg
        self.ref = ref
        self.err = err
        self.logstr = self._get_timeless_log()

    def __str__(self):
        result = self._get_timestamp_format()
        result = result + self._get_timeless_log()
        return result

    def _get_timestamp_format(self):
        return '[' + str(self.timestamp) + ']: '

    def _get_timeless_log(self):
        result = '[' + str(self.lvl) + '] - '
        result = result + str(self.msg)
        if self.ref is not None:
            result = result + "\n\t"
            result = result + str(self.ref)
        if self.err is not None:
            if isinstance(self.err, Exception):
                result = result + "\n\t"
                result = result + str(self.err.args[0])
        return result

class LogLevel(Enum):
    ERROR = 0
    WARN = 1
    DEBUG = 2
    SUCCESS = 3