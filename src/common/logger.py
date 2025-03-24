import logging
from logging import Logger
from logging.handlers import TimedRotatingFileHandler
from pydantic import BaseModel
from pythonjsonlogger import jsonlogger


class LoggerConfig(BaseModel):
    level: str = "DEBUG"
    filename: str = "app.log"
    file_rotating_when: str = "midnight"
    file_rotating_backup_count: int = 7
    file_encoding: str = "utf-8"


def init_logger(cfg: LoggerConfig, logger: Logger):
    logger.setLevel(cfg.level)
    file_handler = TimedRotatingFileHandler(
        filename=cfg.filename,  # 日志文件名
        when=cfg.file_rotating_when,  # 轮换时间：'S' 秒, 'M' 分钟, 'H' 小时, 'D' 天, 'midnight' 午夜
        backupCount=cfg.file_rotating_backup_count,  # 保留的备份文件数量
        encoding=cfg.file_encoding,
    )
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(filename)s %(lineno)d %(funcName)s %(levelname)s %(message)s",
    )
    file_handler.setLevel(cfg.level)
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)

    human_formatter = logging.Formatter(
        fmt="%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s",
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(cfg.level)
    console_handler.setFormatter(human_formatter)
    logger.addHandler(console_handler)
