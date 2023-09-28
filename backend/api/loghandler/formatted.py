from api.loghandler.log import Log, LogLevel
from api.loghandler.loghandler import LogHandler


class FormattedLogHandler(LogHandler):
    class Color:
        # NON RESERVED
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        # RESERVED
        WARNING = '\033[93m'
        ERROR = '\033[91m'
        ENDC = '\033[0m'
        # MISC
        HEADER = '\033[95m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    _color_dates: bool = False
    _color_logs: bool = True
    _default_timestamp_color: Color = Color.BOLD

    def handle(self, log: Log):
        log_col = ''
        ts_col = FormattedLogHandler._default_timestamp_color if FormattedLogHandler._color_dates else ''
        if FormattedLogHandler._color_logs:
            match log.lvl:
                case LogLevel.DEBUG:
                    log_col = FormattedLogHandler.Color.BLUE
                case LogLevel.WARN:
                    log_col = FormattedLogHandler.Color.WARNING
                    ts_col = FormattedLogHandler.Color.WARNING
                case LogLevel.ERROR:
                    log_col = FormattedLogHandler.Color.ERROR \
                        + FormattedLogHandler.Color.UNDERLINE
                    ts_col = FormattedLogHandler.Color.ERROR  \
                        + FormattedLogHandler.Color.UNDERLINE
                case LogLevel.SUCCESS:
                    log_col = FormattedLogHandler.Color.GREEN
                    ts_col = FormattedLogHandler.Color.GREEN
        message = FormattedLogHandler._apply_color(log._get_timeless_log(), log_col)
        timestamp = FormattedLogHandler._apply_color(log._get_timestamp_format(), ts_col)
        print(timestamp + message)

    def set_color_dates(self, val: bool):
        FormattedLogHandler._color_dates = val
        return self

    def set_color_logs(self, val: bool):
        FormattedLogHandler._color_logs = val
        return self

    @staticmethod
    def _apply_color(text, color):
        return str(color) + str(text) + FormattedLogHandler.Color.ENDC
    

