#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import
__author__ = 'dozy-sun'
from datetime import  timedelta
from celery.schedules import crontab


#celery需要引入的包含任务的文件
TASKS_LIST = ['celery_tasks.tasks']

#定时任务
Timing_task={
        # "top_user": {
        #         "task": "celery_tasks.tasks_crontab.top_user_task",
        #         # "schedule": timedelta(seconds=60),
        #         # "schedule":crontab(minute='*/10',hour='3,17,22',day_of_week='thu,fri'),Execute every ten minutes, but only between 3-4 am, 5-6 pm and 10-11 pm on Thursdays or Fridays.
        #         "schedule":crontab(minute=0, hour=0, day_of_week='*'),
        #         },

    }
