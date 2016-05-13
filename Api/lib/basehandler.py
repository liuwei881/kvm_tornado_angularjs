# -*- coding: utf-8 -*-
__author__ = 'Hipeace86'
__datetime__ = '16-3-9'

import tornado


# import json
# import re
# import uuid
# from lib.RedisCache import RightsCache,RedisCache

class CurrentUser(object):
    def __init__(self, uid=None):
        self.Uid = uid

_Current_User = CurrentUser(None)


class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *argc, **argkw):
        super(BaseHandler, self).__init__(*argc, **argkw)

        _Current_User.Uid = self.get_current_user()
        self._PageSize = 15
        self.Result = {'status': 200, 'rows': [], 'total': 0, 'info': 'ok'}

    @property
    def db(self):
        return self.application.db

    @property
    def Redis(self):
        return self.application.Redis

    @property
    def PageSize(self):
        return self.__PageSize

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        return user_id

    def on_finish(self):
        self.db.close_all()

    def write_error(self, status_code, **kwargs):
        import traceback
        exc_info = kwargs["exc_info"]
        trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
        request_info = ''.join(
            ["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k]) for k in self.request.__dict__.keys()])
        error = exc_info[1]

        self.set_header('Content-Type', 'text/html')
        self.finish("""<html>
                         <title>%s</title>
                         <body>
                            <h2>Error</h2>
                            <p>%s</p>
                            <h2>Traceback</h2>
                            <p>%s</p>
                            <h2>Request Info</h2>
                            <p>%s</p>
                         </body>
                       </html>""" % (error, error,
                                     trace_info, request_info))


class RESTfulHandler(BaseHandler):
    RightEnable = True
    OwnerEnable = True
    SortOrder = None

    @tornado.web.authenticated
    def prepare(self):
        # self.request.method = self.get_argument('_method','get')
        self.CheckRith()

    def CheckRith(self):
        if self.RightEnable:
            if self.get_current_user() == '1':
                return True
                # try:
                #     Rights = RightsCache.get("User%sRight"%(self.get_current_user()))
                #     Rights = json.loads(Rights)
                #     url = self.request.uri
                #     for key in Rights.keys():
                #         if re.match('^{0}$'.format(key),url.split('?')[0]) ==None:
                #             continue
                #         else:
                #             if self.request.method.lower() in Rights[key]:
                #                 return True
                #             else:
                #                 self.finish({'errorMsg':'权限不足，不能进行该操作！','errorno':10000,'success':False})
                #     self.finish({'errorMsg':'权限不足，不能进行该操作！','errorno':10000,'success':False})
                # except TypeError,e:
                #     self.finish({'errorMsg':'登陆过期，请重新登陆！','errorno':10001,'success':False})
                #     return False
