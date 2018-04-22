import logging
import platform
import datetime
import pickle
import os


class loghandle():
    _logo_entity = ""

    def __init__(self):
        self.BLACK, self.RED, self.GREEN, self.YELLOW, self.BLUE, self.MAGENTA, self.CYAN, self.WHITE = range(8)
        self.COLORS = {
            'WARNING': self.YELLOW,
            'INFO': self.GREEN,
            'DEBUG': self.BLUE,
            'CRITICAL': self.RED,
            'ERROR': self.RED
        }
        self.RESET_SEQ = "\033[0m"
        self.COLOR_SEQ = "\033[1;%dm"
        self.BOLD_SEQ = "\033[1m"
        self.level = "INFO"

        # datefmt = '%a, %d %b %Y %H:%M:%S'

        self.logger = logging.getLogger("mylogger")
        self.console = logging.StreamHandler()
        self.logger.addHandler(self.console)
        #self.logger.setLevel(logging.INFO)
        self.logger.setLevel(logging.DEBUG)


    @staticmethod
    def getLogEntity():
        if loghandle._logo_entity == "":
            loghandle._logo_entity = loghandle()

        return loghandle._logo_entity

    def output(self, msg, level="INFO", showtime=True, showlevel=True, showcolor=True):
        formatter = '%(message)s'
        if showlevel:
            formatter = '[%(levelname)s] ' + formatter
        if showtime:
            nowtime = datetime.datetime.now().strftime('%H:%M:%S')
            formatter = '[' + nowtime + '] ' + formatter

        if showcolor and platform.system() != "Windows":
            formatter = self.COLOR_SEQ % (
                30 + self.COLORS[level]) + formatter + self.RESET_SEQ

        formatter = logging.Formatter(formatter)
        self.console.setFormatter(formatter)

        if level == "WARNING":
            self.logger.warning(msg)
        elif level == "INFO":
            self.logger.info(msg)
        elif level == "DEBUG":
            self.logger.debug(msg)
        elif level == "CRITICAL":
            self.logger.critical(msg)
        elif level == "ERROR":
            self.logger.error(msg)


if __name__ == "__main__":
    plog = loghandle.getLogEntity()
    plog = loghandle.getLogEntity()
    plog = loghandle.getLogEntity()
    plog = loghandle.getLogEntity()
    plog = loghandle.getLogEntity()
    plog = loghandle.getLogEntity()

    plog.output("aa11a", level="WARNING", showtime=False)
