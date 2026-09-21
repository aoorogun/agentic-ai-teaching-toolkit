from __future__ import annotations
import json
import logging
import os
from datetime import datetime, timezone


def build_logger(name: str, log_dir: str = "logs") -> logging.Logger:
    os.makedirs(log_dir, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        file_path = os.path.join(log_dir, f"{name}.log")
        handler = logging.FileHandler(file_path)
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def log_event(logger: logging.Logger, event_type: str, payload: dict) -> None:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "payload": payload,
    }
    logger.info(json.dumps(record))
