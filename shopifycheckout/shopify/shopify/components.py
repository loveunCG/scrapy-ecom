import traceback
import logging
import os
import datetime
import uuid
from abc import ABC, abstractmethod
from shopify.exceptions import InitializationError, ConfigError, ConnectionError, IOError


class _status:
    code = -1
    msg = ''

    def __str__(self):
        return "{}: {}\n".format(self.code, self.msg)


def monitor(subsystem):
    def wrapper(component):
        try:
            subsystem(component)
        except:
            component.log.error(traceback.format_exc())

    return wrapper


class Component(ABC):
    name = ''
    uid = None

    def __init__(self, *args, **kwargs):
        self._status = _status()

        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)

        self.logFormatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        # file handler
        self.fileHandler = logging.FileHandler("logs/{}_{}.log".format(self.name, self.uid))
        self.fileHandler.setLevel(logging.DEBUG)
        self.fileHandler.setFormatter(self.logFormatter)
        self.log.addHandler(self.fileHandler)

    """ basic operations """

    @monitor
    def load(self):
        return self._load()

    @abstractmethod
    def _load(self):
        pass

    @monitor
    def connect(self):
        return self._connect()

    @abstractmethod
    def _connect(self):
        pass

    def run(self):
        self.load()
        self.connect()

    #   status codes for possible states    """
    #   Errors :                            """
    #   code: -1: Undefined, Component hasn't been initialized
    #         -2: Connection failure
    #         -3: Critical failure
    #   Non-errors :
    #   code:  0: status OK. This case message field can contain any additional info
    #          1: working status, important message/s
    #          2: Handled critical failure, restart required
    #

    # @monitor
    # @abstractmethod
    # def read(self):
    #     pass
    #
    # @monitor
    # @abstractmethod
    # def write(self):
    #     pass

    # TODO add maintanance methods
    # @monitor
    # @abstractmethod
    # def reboot(self):
    #     pass
    #
    # @monitor
    # @abstractmethod
    # def halt(self):
    #     pass

    @property
    def status(self):
        return self._status.code

    @property
    def message(self):
        return self._status.msg

    def _set_status(self, code, message=''):
        """ method to set status/message of component in extra cases like reboot    """
        self._status.code = code
        self._status.msg = message

    def diagnostic(self):
        return self.status


class CrawlerComponent(Component):
    name = 'crawler'
    uid = uuid.uuid4()

    def _connect(self):
        self.log.info("Connection successfully established")

    def _load(self):
        self.log.info("Crawler loaded.\n")