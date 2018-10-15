class ConfigError(Exception):
    """ Raises in case of wrong config files """
    pass

class InitializationError(Exception):
    """ Raises in case of components loading issue """
    pass

class ConnectionError(Exception):
    """ Raises in case of connection troubles """
    pass

class IOError(Exception):
    """ Raises in case of IO error """
    pass