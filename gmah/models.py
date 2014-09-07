# -*- coding:utf-8 -*-
# coding=<utf8>

from django.db import models # django.db.models.Model
from django.utils.timezone import make_aware, get_current_timezone, is_aware, is_naive
from settings import BASE_DIR, DATABASES, MEDIA_ROOT

def content_file_name(instance, filename):
    a = instance.timestamp
    # c = make_aware(a,get_current_timezone())
    # b = str(c)
    b = str(a)
    # d1 = is_aware(a)
    # d2 = is_naive(a)

    # raise NotImplementedError('RuntimeError')
    d = '_'.join((b.split(' ')[0],'_'.join(b.split(' ')[1].split('.')[0].split(':')),b.split(' ')[1].split('.')[1].split('+')[0]))
    # return '/claim_files/'+'_'.join([ d, filename])
    # a = '/claim_files/'+d+'.jpg'
    # raise ImportError(a)
    # return '/usr/home/ishayahu/gmah/claim_files/claim_files/'+d+'.jpg'
    return MEDIA_ROOT+'/claim_files/'+d+'.jpg'

    # return '/media/'+d+'.jpg'
    # WORKING
    # return d+'.jpg'
class File(models.Model):
    timestamp = models.DateTimeField()
    file_name = models.CharField(max_length=140)
    # file = models.FileField(upload_to='claim_files') # add separation by tasks
    file = models.FileField(upload_to=content_file_name) # add separation by tasks
    description = models.TextField()
    class Meta:
        ordering = ['timestamp']
    def __unicode__(self):
        return str(self.id)+" "+self.file_name
    # @models.permalink
    def get_absolute_url(self):
        return "/media/claim_files/%s.jpg" % self.file_name

class Person(models.Model):
    fio = models.CharField(max_length=140)
    tel = models.CharField(max_length=10)
    mail = models.EmailField(blank = True, null = True)
    raiting = models.CharField(max_length=30, blank = True, null = True)
    login = models.CharField(max_length=140)
    # для каких заявок отправлял запрос на предоставление данных
    acl = models.TextField(default=False)
    def __unicode__(self):
        return ";".join((self.fio,str(self.login)))
    class Meta:
        ordering = ['fio',]
class Claim(models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(blank = True, null = True)
    # category = models.ForeignKey(Categories)
    open_date = models.DateTimeField()
    close_date = models.DateTimeField(blank = True, null = True)
    # Правильное название!!!!!!!
    owner = models.ForeignKey(Person, related_name = "claims_for_person")
    closed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    acl = models.TextField(default=False) # кто может смотреть данные хозяина заявки
    file = models.ManyToManyField(File, related_name = "for_claim", blank = True, null = True)
    def __unicode__(self):
        return u";".join((str(self.id),self.name,"\t"+self.owner.fio))
    class Meta:
        ordering = ['id','open_date']
class Requests(models.Model):
    claim = models.ForeignKey(Claim, related_name = "claim_for_request",)
    claim_owner = models.ForeignKey(Person, related_name = "claim_owner",)
    person = models.ForeignKey(Person, related_name = "request_owner",)
    date = models.DateTimeField()
    seen = models.BooleanField(default=False)
    def __unicode__(self):
        return u"from %s to %s claim %s" % (self.person.login,
                                            self.claim_owner.login,
                                            self.claim.id)