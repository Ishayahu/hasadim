# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models

class Person(models.Model):
    fio = models.CharField(max_length=140)
    tel = models.CharField(max_length=10)
    mail = models.EmailField(blank = True, null = True)
    raiting = models.CharField(max_length=30, blank = True, null = True)
    login = models.CharField(max_length=140, blank = True, null = True)
    def __unicode__(self):
        return ";".join((self.fio,str(self.login)))
    class Meta:
        ordering = ['fio',]
