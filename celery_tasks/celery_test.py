#!/usr/bin/env python2.7
# encoding:utf-8

from __future__ import absolute_import

__author__ = 'dozy-sun'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
import tcelery
from celery_tasks import tasks
from celery_tasks.tasks import add
from functools import partial
from celery import group,chain,chord

from tornado.options import define, options
define("port", default=9000, help="run on the given port", type=int)

tcelery.setup_nonblocking_producer()


class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        print 'add'
        chain(add.s(2, 2), add.s(4), add.s(8)).get()
        group(tasks.add.subtask(i) for i in xrange(10)).apply_async()
        esult = tasks.add.apply_async((2, 2),  countdown=3, expires=60, retry=True, retry_policy={
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.2,
        })
        a = tasks.add.apply_async(args=[5, 6])
        print 'done'
        print a.result
        self.write("when i sleep 5s")
        self.write('%s' % self.request.headers.keys())
        self.finish()

class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you")

class AsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        tasks.add.apply_async(args=[5,6], callback=self.on_result)

    def on_result(self, response):
        self.write(str(response.result))
        self.finish()

class SleepAsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        print 'add'
        response = tasks.add.apply_async(args=[5, 6])
        tornado.ioloop.IOLoop.instance().call_later(2, partial(self.on_delay_celery_result, response))

    def on_delay_celery_result(self, response):
        if not response.result:
            tornado.ioloop.IOLoop.instance().call_later(2, partial(self.on_delay_celery_result, response))
        else:
            print response.result
            self.on_result(response)

    def on_result(self, response):
        print 'done'
        self.write("when i sleep 5s 5+6 = %s" % response.result)
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler),
            (r"/justnow", JustNowHandler),
            (r"/sleep_s", AsyncHandler),
            (r"/sleeps", SleepAsyncHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print 'start................'
    tornado.ioloop.IOLoop.instance().start()