import logging
import os

import configparser

config = configparser.RawConfigParser()

HERE = os.path.dirname(__file__)

configfiles = [
    '/etc/tictactoe.cfg',                         # staging/live
    os.path.join(HERE, 'tictactoe.default.cfg'),  # default config
    os.path.join(HERE, 'tictactoe.cfg'),          # per-environment config
]

files_read = config.read(configfiles)

logging.debug('config files read: %s' % files_read)
