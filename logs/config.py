import logging.handlers
from loguru import logger
import logging
import os
from src.utils.settings import getSettings
from src.utils.intercept_handler import InterceptHandler
from src.utils.notifier import get_handler

settings = getSettings()
S = os.sep
LOGFILE_PATH = f"{os.path.dirname(__file__)}{S}log_files{S}{settings.APP_NAME}"


def setup():
    # catch logging records
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.add(f"{LOGFILE_PATH}.log", rotation="2 MB",
               compression="zip", level=0)

    logger.debug(f"{LOGFILE_PATH}.log file has been added to logging")

    # logger.add(f"{LOGFILE_PATH}.jsonl", rotation="2 MB",
    #            compression="zip", level="ERROR", serialize=True)

    logger.debug(f"{LOGFILE_PATH}.jsonl file has been added to logging")
    # add telegram notifications for critical records
    logger.add(get_handler(), level="CRITICAL")

    logger.trace("logging setup complete")
