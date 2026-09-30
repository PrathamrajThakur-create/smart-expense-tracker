"""Central logging setup (rotating file, so logs never grow unbounded)."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str = "expense_tracker", log_dir: str = "logs") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # already configured
        return logger
    logger.setLevel(logging.INFO)
    try:
        Path(log_dir).mkdir(exist_ok=True)
        handler = RotatingFileHandler(Path(log_dir) / "app.log",
                                      maxBytes=200_000, backupCount=2)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    except OSError:
        logger.addHandler(logging.NullHandler())
    return logger
