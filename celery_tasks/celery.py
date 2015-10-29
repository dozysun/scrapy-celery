#!/usr/bin/env python2.7
#encoding:utf-8

from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

from celery import Celery
from kombu import serialization,Exchange, Queue
from settings import BACKEND_URL,BROKER_URL
from celery_tasks.setting import Timing_task,TASKS_LIST
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# serialization.registry._disabled_content_types.remove('application/x-python-serialize')
# register('ujson', ujson.dumps, ujson.loads,
#     content_type='application/json',
#     content_encoding='utf-8')


app = Celery('tasks',
             backend=BACKEND_URL,
             broker=BROKER_URL,
             include= TASKS_LIST
)

app.conf.update(

    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    # CELERY_TIMEZONE='Europe/Oslo',
    # CELERY_ENABLE_UTC=True,

    #定义消息队列
    CELERY_DEFAULT_QUEUE='default',
    CELERY_QUEUES=(
        Queue('default', routing_key='task.#'),
        Queue('feed_tasks', routing_key='feed.#'),
    ),
    CELERY_DEFAULT_EXCHANGE='tasks',
    CELERY_DEFAULT_EXCHANGE_TYPE='topic',
    CELERY_DEFAULT_ROUTING_KEY='task.default',

    #定义路由  将任务路由到指定的queue
    CELERY_ROUTES = {
    #     'celery_tasks.tasks.sleep':  {'queue': 'default', 'routing_key': 'task.sleep'},
        'celery_tasks.tasks.add': {'queue': 'feed_tasks', 'routing_key': 'feed.add'},
    },

    #broker setting
    #连接超时时间 默认4,单位s
    # BROKER_CONNECTION_TIMEOUT = 1,

    #取消速率限制
    # CELERY_DISABLE_RATE_LIMITS = True,

    #使用本地时间,默认使用utc
    CELERY_ENABLE_UTC = False,

    #定义定时任务
    CELERYBEAT_SCHEDULE = Timing_task,

    #是否允许远程控制 默认为ture
    # CELERY_ENABLE_REMOTE_CONTROL=False,

    #是否允许远程控制 重启服务 默认Flase
    CELERYD_POOL_RESTARTS=True,

    #定义错误信息的邮件服务
    # # Enables error emails.
    # CELERY_SEND_TASK_ERROR_EMAILS = True,
    #
    # # Name and email addresses of recipients
    # ADMINS = (
    #     ('George Costanza', 'george@vandelay.com'),
    #     ('Cosmo Kramer', 'kosmo@vandelay.com'),
    # ),


    # # Email address used as sender (From field).
    # # SERVER_EMAIL = 'no-reply@vandelay.com',
    # ADMINS = [('_', 'dozysun@gmail.com')],
    # # Mailserver configuration
    # EMAIL_HOST = 'mail.vandelay.com',
    # EMAIL_PORT = 25,
    # EMAIL_HOST_USER = 'servers'
    # EMAIL_HOST_PASSWORD = 's3cr3t'
)

if __name__ == '__main__':
    app.start()

# celery -A celery_tasks worker -B -Q default,feed_tasks -l info
# celery flower -A celery_tasks -port=5555 --basic_auth=username:pwd,username2:pwd2
# ps auxww | grep 'celery' | awk '{print $2}' | xargs kill -9
# self.app - Celery  self - Task  self.request - 请求

