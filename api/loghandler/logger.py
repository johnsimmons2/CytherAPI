from datetime import datetime
from api.loghandler.log import LogLevel, Log
from api.loghandler.loghandler import LogHandler


class Logger:
    _handler = None
    _handler_validated = False

    @staticmethod
    def _log(log: Log):
        if Logger._handler_validated or Logger._handler is not None:
            # If there is a log handler set up.
            Logger._handler_validated = True
            handler = Logger._handler
            handler.handle(log)
        else:
            # Basic control is to print stringified log.
            print(str(log))

    @staticmethod
    def log(lvl: LogLevel, msg: str, ref: any = None, err: any = None, time: datetime = None):
        Logger._log(Log(lvl, msg, ref, err, time))

    @staticmethod
    def debug(msg: str, ref:any = None, err: any = None, time: datetime = None):
        Logger.log(LogLevel.DEBUG, msg, ref, err, time)

    @staticmethod
    def warn(msg: str, ref:any = None, err: any = None, time: datetime = None):
        Logger.log(LogLevel.WARN, msg, ref, err, time)

    @staticmethod
    def error(msg: str, ref:any = None, err: any = None, time: datetime = None):
        Logger.log(LogLevel.ERROR, msg, ref, err, time)

    @staticmethod
    def success(msg: str, ref:any = None, err: any = None, time: datetime = None):
        Logger.log(LogLevel.SUCCESS, msg, ref, err, time)

    @staticmethod
    def config_set_handler(handler):
        if isinstance(type(handler), type(LogHandler)):
            Logger._handler = handler
            Logger.debug('Setup log handler - ' + str(type(handler)))
        else:
            raise TypeError('Cannot set log handler to invalid log handler object type')