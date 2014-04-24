import logging
import os

import configparser

config = configparser.RawConfigParser()

HERE = os.path.dirname(__file__)

configfiles = [
    os.path.join(HERE, 'tictactoe.default.cfg'),  # default config
    os.path.join(HERE, 'tictactoe.cfg'),          # per-environment config
    '/etc/tictactoe.cfg',                         # staging/live
]

files_read = config.read(configfiles)

logging.debug('config files read: %s' % files_read)
