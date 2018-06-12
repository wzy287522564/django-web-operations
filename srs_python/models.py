# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Create your models here.

class ProfileBase(type):  # 对于传统类，他们的元类都是types.ClassType
    def __new__(cls, name, bases, attrs):  # 带参数的构造器，__new__一般用于设置不变数据类型的子类
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b, ProfileBase)]
        if parents:
            fields = []
            for obj_name, obj in attrs.items():
                if isinstance(obj, models.Field): fields.append(obj_name)
                User.add_to_class(obj_name, obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name, {'fields': fields}))
        return super(ProfileBase, cls).__new__(cls, name, bases, attrs)


class ProfileUser(object):
    __metaclass__ = ProfileBase  # 类属性


class MyProfile(ProfileUser):
    qq = models.CharField(max_length=16,blank=True)  # qq
    weChat = models.CharField(max_length=100,blank=True) #微信
