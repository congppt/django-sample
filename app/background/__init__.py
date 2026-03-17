from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task, on_commit_task, lock_task, task, signal
from huey.signals import SIGNAL_CANCELED, SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_REVOKED

from utils.log import logger

@signal(SIGNAL_ERROR, SIGNAL_LOCKED, SIGNAL_CANCELED, SIGNAL_REVOKED)
def task_not_executed_handler(signal, task_instance, exc=None):
   logger.opt(exception=exc).error(f"Task {getattr(task_instance, 'name', task_instance.id)} not executed: {signal}")