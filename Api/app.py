# -*- coding: utf-8 -*-

__author__ = 'Hipeace86'
__datetime__ = '16-3-9'

import sys

import tornado.ioloop
import tornado.httpserver
import tornado.web
from tornado.options import options, define, parse_command_line
import os
from lib.LoginHandler import LoginHandler
from lib.urlmap import urlmap
from lib.Route import db_session

# 动态加载应用，主要导入URL配置
root = os.getcwd()
Dirs = [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
for d in Dirs:
    if os.path.isdir(os.path.join(root, d, 'Handler')):
        exec('import %s.Handler' % (d,))


class Application(tornado.web.Application):
    def __init__(self):
        handlers = tuple(urlmap.handlers)
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True,
            xsrf_cookies=True,
            autoescape=None,
            login_url='/#/login',
            cookie_secret='61oETzKXQAGaYdkL5gEmGEJJFuYh7EQnp2XdTP1o/Vo=',
        )
        self.db = db_session
        tornado.ioloop.PeriodicCallback(self._ping_db, 4 * 3600 * 1000).start()
        tornado.web.Application.__init__(self, handlers, **settings)

    def _ping_db(self):
        self.db.execute('show variables')
        self.db.close_all()


define('port', type=int, default=4002)


def main():
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    main()
