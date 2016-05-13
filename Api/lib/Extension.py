# -*- coding: utf-8 -*-
__author__ = 'Hipeace86'
__datetime__ = '15-4-13'

from sqlalchemy.orm.interfaces import MapperExtension
from lib.basehandler import _Current_User


class DataUpdateExtension(MapperExtension):
    def before_update(self, mapper, connection, instance):
        if hasattr(instance, 'UpdateId'):
            instance.UpdateId = _Current_User.Uid

    def before_insert(self, mapper, connection, instance):
        if hasattr(instance, 'CreateId'):
            instance.CreateId = _Current_User.Uid
            if hasattr(instance, 'UpdateId'):
                instance.UpdateId = instance.CreateId
