#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
import tcelery
from celery_tasks import tasks
from functools import partial

from tornado.options import define, options
define("port", default=9000, help="run on the given port", type=int)

tcelery.setup_nonblocking_producer()


class SleepHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        print 'add'
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