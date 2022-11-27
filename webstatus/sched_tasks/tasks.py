import dramatiq
import time
import logging

from django_dramatiq.tasks import delete_old_tasks

@dramatiq.actor
def dramatiq_delete_old_tasks():
    delete_old_tasks.send(max_task_age=86400)
    return 0

@dramatiq.actor()
def test_heartbeat():
    logging.warning('Start heartbeat task')
    time.sleep(10)
    logging.warning('End heartbeat task')
    return 0
    