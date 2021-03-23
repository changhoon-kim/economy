import logging
import os

from logging.handlers import TimedRotatingFileHandler

Logger = logging.getLogger()

def setup_logging():
    Logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    Logger.addHandler(ch)

    log_dir = os.path.abspath(os.path.join(__file__, '..', 'logs'))
    log_file = '%s/economy.log' % log_dir
    if not os.path.isfile(log_file):
        os.makedirs(log_dir)

    fh = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=93)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    Logger.addHandler(fh)
