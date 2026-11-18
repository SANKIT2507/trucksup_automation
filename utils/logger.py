"""
TrucksUp Automation - Logger Utility
=====================================
"""

import logging


def get_logger(name="TrucksUp"):
    """Custom logger create karo"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
