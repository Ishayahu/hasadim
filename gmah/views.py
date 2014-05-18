# -*- coding:utf-8 -*-
# coding=<utf8>

#TODO: сделать возможность изменения языков

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
import datetime

from settings import BASE_DIR, DATABASES
from gmah.models import Person

def tasks(request):
	now = datetime.datetime.now()
	html = "<html><body>Now: %s <p> BASE_DIR %s<p> DATABASES %s </body></html>" % (now,BASE_DIR,DATABASES)
	return HttpResponse(html)
	