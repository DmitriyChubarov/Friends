# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser 

class Users(AbstractUser):

    def __str__(self):
	    return self.username

class Prop(models.Model):
    out_id = models.ForeignKey(Users,
                               on_delete=models.CASCADE,
                               null=False,
                               related_name='out_user')
    in_id = models.ForeignKey(Users,
                               on_delete=models.CASCADE,
                               null=False,
                               related_name='in_user')
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.out_id.username

class Friends(models.Model):
    first_id = models.ForeignKey(Users,
                                 on_delete=models.CASCADE,
                                 null=False,
                                 related_name='first_friend')

    second_id = models.ForeignKey(Users,
                                 on_delete=models.CASCADE,
                                 null=False,
                                 related_name='second_friend')
