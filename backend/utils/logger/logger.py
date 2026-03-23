from .tg_handler import TelegramHandler

from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import colorlog
import logging
import os

load_dotenv()


def make_logger(name: str, use_telegram: bool = False, log_dir: str = 'logs') -> logging.Logger:

    logger = logging.getLogger(name)
    logger.propagate = False

    if not logger.hasHandlers():
        log_level = os.getenv("LOG_LEVEL", "DEBUG").upper()
        logger.setLevel(getattr(logging, log_level, logging.DEBUG))

        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"{name}.log")

        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - [%(filename)s:%(lineno)d - %(funcName)s] - %(levelname)s - %(message)s',

            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'bold_yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red',
            }
        ))

        logger.addHandler(handler)

        file_handler = RotatingFileHandler(
            log_file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding='utf-8'
        )

        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
            )
        )
        logger.addHandler(file_handler)

        if use_telegram:

            tg_token = os.getenv('TG_TOKEN')
            tg_chat_id = os.getenv('MY_TG_CHAT_ID')

            if tg_token and tg_chat_id:
                tg_handler = TelegramHandler(
                    token=tg_token, chat_id=tg_chat_id)

                tg_handler.setFormatter(logging.Formatter(
                    '%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
                ))

                logger.addHandler(tg_handler)

            else:
                logger.warning("❗ TG_TOKEN или TG_CHAT_ID не заданы в .env")

    return logger
