import logging
import os

import configparser

config = configparser.RawConfigParser()

HERE = os.path.dirname(__file__)

configfiles = [
    '/etc/challenge.cfg',                         # staging/live
    os.path.join(HERE, 'challenge.default.cfg'),  # default config
    os.path.join(HERE, 'challenge.cfg'),          # per-environment config
]

files_read = config.read(configfiles)

logging.debug('config files read: %s' % files_read)
