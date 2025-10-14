from datetime import timedelta
import os
import sys

from loguru import logger as __logger

from env import IS_LOCAL, LOG_DIR

# Set traceback limit
sys.tracebacklimit = 1
# Create log directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)
# Remove default handler
__logger.remove(0)
# Default log options
__log_opts= dict(
    rotation=timedelta(days=1),
    retention=timedelta(days=90),
    enqueue=True,
    format="{message}",
    encoding="utf-8",
    serialize=True,
)

# Standard logger
__logger.add(
    os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.json"),
    level="INFO",
    **__log_opts,
)

# Error logger
__logger.add(
    os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.error.json"),
    level="ERROR",
    **__log_opts,
)

# API call logger
__logger.add(
    os.path.join(LOG_DIR, "{time:YYYY-MM-DD}.api.json"),
    level="INFO",
    filter=lambda record: record["extra"].get("type") == "api",
    **__log_opts,
)

# Discord logger
if not IS_LOCAL:
    # async def notify(message):
    #     await discord.send_notification(f"`{ENV}`{message}")
    # __logger.add(
    #     notify,
    #     level="ERROR",
    #     format="{message}\n Details: {extra}\n",
    #     enqueue=True,
    # )
    pass

# Console logger
__logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{module}.{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> {extra}",
    level="DEBUG",
    enqueue=True,
)

logger = __logger
