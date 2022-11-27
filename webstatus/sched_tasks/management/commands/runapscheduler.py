# runapscheduler.py
import logging
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

import sched_tasks.tasks

logger = logging.getLogger(__name__)


def test_job_in_runapscheduler():
  # Your job processing logic here...
  time.sleep(3)
  pass


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way. 
@util.close_old_connections
def apscheduler_delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
    scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
      test_job_in_runapscheduler,
      trigger=CronTrigger(minute="*", second="0"),
      id="test_job_in_runapscheduler",  # The `id` assigned to each job MUST be unique
      max_instances=1,
      replace_existing=True,
    )
    self.stdout.write("Added job 'test_job_in_runapscheduler'.")

    scheduler.add_job(
      apscheduler_delete_old_job_executions,
      trigger=CronTrigger(
        # Midnight on Monday, before start of the next work week.
        day_of_week="mon", hour="00", minute="00"
      ),
      id="delete_old_job_executions",
      max_instances=1,
      replace_existing=True,
    )
    self.stdout.write("Added weekly job: 'apscheduler_delete_old_job_executions'.")

    scheduler.add_job(
      sched_tasks.tasks.dramatiq_delete_old_tasks,
      trigger=CronTrigger(
        # Midnight on Monday, before start of the next work week.
        day_of_week="mon", hour="00", minute="00"
      ),
      id="dramatiq_delete_old_tasks",
      max_instances=1,
      replace_existing=True,
    )
    self.stdout.write("Added weekly job: 'dramatiq_delete_old_tasks'.")

    try:
      self.stdout.write("Starting scheduler...")
      scheduler.start()
    except KeyboardInterrupt:
      self.stdout.write("Stopping scheduler...")
      scheduler.shutdown()
      self.stdout.write("Scheduler shut down successfully!")
      