# -*- coding:utf-8 -*-
# coding=<utf8>

#TODO: сделать возможность изменения языков

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from PIL import Image
import datetime

# Делаем переводы
from djlib.multilanguage_utils import select_language,multilanguage,register_lang, get_localized_form#,register_app
from djlib.cron_utils import decronize, crontab_to_russian, generate_next_reminder
from djlib.text_utils import htmlize, what_to_people_friendly
from djlib.acl_utils import  for_admins, admins_only
# from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log, make_request_with_logging
from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors
from django.utils.timezone import make_aware, get_current_timezone, is_aware, is_naive


from settings import BASE_DIR, DATABASES
from gmah.models import Person, Claim, File

register_lang('ru','RUS')
register_lang('eng','ENG')
app='gmah'

def save_file(files,id):
    a = datetime.datetime.now()
    c = make_aware(a,get_current_timezone())
    b = str(c)
    d1 = is_aware(c)
    d2 = is_naive(c)
    d = '_'.join((b.split(' ')[0],'_'.join(b.split(' ')[1].split('.')[0].split(':')),b.split(' ')[1].split('.')[1].split('+')[0]))
    # fn = '_'.join([ c, filename])
    # raise NotImplementedError('a')
    instanse = File(file=files['file'],
                    timestamp=c,
                    file_name = 'img_for_'+str(d),
                    description = 'image for '+str(id),)
    instanse.save()
    path_to_file = instanse.file.path
    print path_to_file
    img=Image.open(path_to_file)
    img.thumbnail((100,100),Image.ANTIALIAS)
    img.save(path_to_file,'JPEG')

    return instanse

# @login_required
@multilanguage
# @shows_errors
# @for_admins
def main(request):
    claims =  Claim.objects.filter(deleted=False).filter(closed=False)
    return (True,('main.html',{},{'title':'GMAH.RU','claims':claims,},request,app))
@login_required
@multilanguage
def claim_add(request):
    if request.method == 'POST':
        open_date = datetime.datetime.now()
        form = get_localized_form('NewClaimForm',app,request)(request.POST)
        lang,user,fio,method = get_info(request)
        if form.is_valid():
            data = form.cleaned_data
            # a = datetime.datetime.now()
            open_date = make_aware(open_date,get_current_timezone())

            new_claim=Claim(name=data['name'], 
                        description = data['description'],
                        open_date = open_date,
                        owner = fio)
            new_claim.save()
            if request.FILES:
                new_claim.file.add(save_file(request.FILES,new_claim.id))
            new_claim.save()
            return (False,HttpResponseRedirect('/'))
        return (False,HttpResponseRedirect('/'))   
    return (True,('claim_add.html',{'NewClaimForm':{}},{'title':'GMAH.RU - добавить заявку',},request,app))
@login_required
@multilanguage
def claim_edit(request,id):
    try:
        claim = Claim.objects.get(id=id)
    except Task.DoesNotExist:
        add_error(u"Заявка с номером %s не найдена!" % id,request)
        # return (False,(HttpResponseRedirect("/assets_by_type/"+type_id+"/")))
        return (False,(HttpResponseRedirect("/")))
    if request.method == 'POST':
        open_date = datetime.datetime.now()
        form = get_localized_form('NewClaimForm',app,request)(request.POST)
        lang,user,fio,method = get_info(request)
        if form.is_valid():
            data = form.cleaned_data
            claim.name =data['name']
            claim.description = data['description']
            claim.save()
            return (False,HttpResponseRedirect('/claim/show/'+str(id)))
        return (False,HttpResponseRedirect('/claim/edit/'+str(id)))   
    return (True,('claim_add.html',{'NewClaimForm':{'name':claim.name, 'description':claim.description}},{'title':'GMAH.RU - добавить заявку',},request,app))
@multilanguage
@shows_errors
def claim_show(request,id):
    try:
        claim = Claim.objects.get(id=id)
    except Task.DoesNotExist:
        add_error(u"Заявка с номером %s не найдена!" % id,request)
        # return (False,(HttpResponseRedirect("/assets_by_type/"+type_id+"/")))
        return (False,(HttpResponseRedirect("/")))
    # a = str(claim.id)
    title = u'GMAH.RU - заявка %s' % str(claim.id)
    files=claim.file.all()
    return (True,('claim_show.html',{},{'title':title ,'claim':claim,'files':files},request,app))
