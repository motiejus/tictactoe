import logging
import os

import configparser

config = configparser.RawConfigParser()

HERE = os.path.dirname(__file__)

configfiles = [
    os.path.join(HERE, 'challenge.default.cfg'),  # default config
    os.path.join(HERE, 'challenge.cfg'),          # per-environment config
    '/etc/gameplatform.cfg'                       # staging/live
]

files_read = config.read(configfiles)

logging.debug('config files read: %s' % files_read)
