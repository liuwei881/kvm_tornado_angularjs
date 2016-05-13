# -*- coding: utf-8 -*-
__author__ = 'Hipeace86'
__datetime__ = '16-3-9'

from lib.urlmap import urlmap
from lib.basehandler import BaseHandler
from tornado import web


@urlmap(r'/login')
class LoginHandler(BaseHandler):
    @web.asynchronous
    def get(self):
        account = self.get_argument('user', '')
        password = self.get_argument('password', '')
        if account == password:
            self.Result['info'] = u'登陆成功'
            self.Result['status'] = 200
            self.xsrf_token
            self.set_secure_cookie('user', account, expires_days=0.5)
        self.finish(self.Result)
