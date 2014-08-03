# -*- coding:utf-8 -*-
# coding=<utf8>

#TODO: сделать английские формы

from django import forms
from gmah.models import Person, Claim
# from tasks.todoes.models import Worker, Client
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm

PRIORITY_CHOICES = (
        ('1','Лазар/Борода/Мотя'),
        ('2','Если не сделать сейчас - огребём проблем потом'),
        ('3','Всё остальное'),
        ('4','В ближайшем будущем'),
        ('5','Когда время будет')
    )

inp_f=( '%d-%m-%Y %H:%M:%S',     # '2006-10-25 14:30:59'
        '%d-%m-%Y %H:%M',        # '2006-10-25 14:30'
        '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30'
        '%d-%m-%Y',              # '2006-10-25'
        '%d/%m/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
        '%d/%m/%Y %H:%M',        # '10/25/2006 14:30'
        '%d/%m/%Y',              # '10/25/2006'
        '%d.%m.%Y %H:%M:%S',     # '10/25/2006 14:30:59'
        '%Y.%m.%d %H:%M:%S',     # '2010/01/26 14:30:59'
        '%d/%m/%y %H:%M:%S',     # '10/25/06 14:30:59'
        '%d/%m/%y %H:%M',        # '10/25/06 14:30'
        '%d/%m/%y',       )
class NewClaimForm(forms.Form):
    name = forms.CharField(max_length=140, label='Название заявки')
    description = forms.CharField(widget=forms.Textarea, label='Описание')
    file  = forms.FileField(label="Прикрепить картинку", required=False)
    file1  = forms.FileField(label="Прикрепить картинку", required=False)
    file2  = forms.FileField(label="Прикрепить картинку", required=False)
    file3  = forms.FileField(label="Прикрепить картинку", required=False)
    def __init__(self,arg_dict):
        count_of_files = arg_dict.pop('count_of_files','')
        field_names = ('file3','file2','file1','file')
        super(NewClaimForm, self).__init__(arg_dict)
        if count_of_files:
            for i in range(count_of_files):
                self.fields.pop(field_names[i])




class UserCreationFormMY(UserCreationForm):
    fio = forms.CharField(label='ФИО')
    mail = forms.EmailField(label = 'Мыло')
    tel = forms.CharField(label='Телефон', max_length=10, min_length=10)
class UserEditForm(forms.Form):
    fio = forms.CharField(label='ФИО')
    mail = forms.EmailField(label = 'Мыло')
    tel = forms.CharField(label='Телефон', max_length=10, min_length=10)
