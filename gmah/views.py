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

def save_file(file_instance,id):
    # размеры итогового файла
    h=480
    w=480
    background_color = "green"
    # background_color = "white"
    a = datetime.datetime.now()
    c = make_aware(a,get_current_timezone())
    b = str(c)
    d1 = is_aware(c)
    d2 = is_naive(c)
    d = '_'.join((b.split(' ')[0],'_'.join(b.split(' ')[1].split('.')[0].split(':')),b.split(' ')[1].split('.')[1].split('+')[0]))
    # fn = '_'.join([ c, filename])
    # raise NotImplementedError('a')
    instanse = File(file=file_instance,
                    timestamp=c,
                    file_name = str(d),
                    description = 'image for '+str(id),)
    instanse.save()
    path_to_file = instanse.file.path
    print path_to_file
    img=Image.open(path_to_file)
    # вычисляем пропорции
    iw, ih = img.size
    ratio = float(max(ih,iw))/h
    new_h = int(round(ih/ratio))
    new_w = int(round(iw/ratio))
    # raise ImportError('')
    img.thumbnail((new_w,new_h),Image.ANTIALIAS)
    # а теперь мы делаем изображение стандартного размера, вставляем в него
    # наше превью, чтобы всё изображения были равного размера, а пустое место
    # будет белым
    a=Image.new("RGB",(w,h),background_color)
    # вычисляем куда вставлять картинку
    ins_h = 0
    ins_w = 0
    if new_w > new_h: # значит, картинка в ширину и надо вставить по середине высоты
        ins_h = int(round((h-new_h)/2))
    if new_w < new_h: # значит, картинка в высоту и надо вставить по середине ширины
        ins_w = int(round((w-new_w)/2))
    a.paste(img,(ins_w,ins_h))
    a.save(path_to_file,'JPEG')
    # img.save(path_to_file+'test.jpeg','JPEG')
    
    
    
    
    
    
    # img.save(path_to_file,'JPEG')
    
    # im.paste(image, box)
    
    
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
            a = request.FILES
            if request.FILES:
                for filed in ('file','file1','file2','file3'):
                    if filed in request.FILES:
                        print request.FILES[filed]
                        new_claim.file.add(save_file(request.FILES[filed],new_claim.id))
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
    first_file = files[0]
    files = files[1:]
    return (True,('claim_show.html',{},{'title':title ,'claim':claim,'files':files,'first_file':first_file},request,app))
