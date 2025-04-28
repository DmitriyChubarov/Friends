# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Users, Prop, Friends

admin.site.register(Users)
admin.site.register(Prop)
admin.site.register(Friends)
# Register your models here.
