import logging


def log_config():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    log = logging.getLogger(__name__)
    return log
