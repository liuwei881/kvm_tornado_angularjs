# -*- coding: utf-8 -*-
__author__ = 'Hipeace86'
__datetime__ = '16-3-6'


class Urlmap(object):
    def __init__(self):
        self.handlers = []
        self.__version__ = 'v2'

    def __call__(self, url, **kwds):
        def _(cls):
            self.handlers.append(("/api/{0}{1}".format(self.__version__, url), cls, kwds))
            return cls

        return _


def handlers(*args):
    handlers = []
    for i in args:
        handlers.extend(i.urlmap.handlers)
    return handlers


urlmap = Urlmap()
