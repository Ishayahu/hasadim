# -*- coding:utf-8 -*-
# coding=<utf8>

# Общий поход к правам доступа:
# TODO при запросе данных к заявке право на просмотр профиля добалвятеся для хоязина заявки для всего профиля

# TODO задать разрешение на просмотр профиля при отправке запроса
# TODO при просмотре профиля если он отправлял запрос на твою...
# заявку - можешь это сделать

# TODO
# TODO
# TODO при разрешении на просмотр контактых данных разрешение добавляется только для это заявки
#
# TODO ТАким образом когда человек хочет посмотреть профиль он это может только если у него этот человек запрашивал данные
# TODO если хочет посмотреть к заявке - только если ему открыли доступ. Прямой связи между профилем и заявкой для людей нет

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
from djlib.acl_utils import  for_admins, admins_only, add_permission, remove_permission
# from djlib.user_tracking import set_last_activity_model, get_last_activities
from djlib.mail_utils import send_email_alternative
from djlib.auxiliary import get_info
from djlib.logging_utils import log, confirm_log, make_request_with_logging
from djlib.error_utils import FioError, ErrorMessage, add_error, shows_errors
from django.utils.timezone import make_aware, get_current_timezone, is_aware, is_naive
from user_settings.settings import admins


from settings import BASE_DIR, DATABASES, MEDIA_ROOT
from gmah.models import Person, Claim, File, Requests

# import the logging library
import logging,sys

# Get an instance of a logger
logger = logging.getLogger(__name__)

register_lang('ru','RUS')
register_lang('eng','ENG')
app='gmah'

@login_required
@multilanguage
@admins_only
def register(request):
    lang=select_language(request)
    if request.method == 'POST':
        # form = UserCreationFormMY(request.POST)
        form = get_localized_form('UserCreationFormMY',app,request)(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_user = form.save()
            new_person = Person(
                fio = data['fio'],
                tel = data['tel'],
                mail = data['mail'],
                login = data['username']
            )
            new_person.save()
            return (False,(HttpResponseRedirect("/")))
    # else:
        # form = l_forms[lang]['UserCreationFormMY']()
    # return render_to_response(languages[lang]+"registration/register.html",{'form':form},RequestContext(request))
    return (True,('register.html',{'UserCreationFormMY':{}},{'title':'GMAH.RU','target':'Создать новый профиль',},request,app))
@login_required
@multilanguage
def profile_redirect(request):
    user = request.user.username
    try:
        profile_owner = Person.objects.get(login=user)
    except Person.DoesNotExist:
        add_error(u"Пользователь с id %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    return (False,(HttpResponseRedirect(
        "/accounts/profile/show/%s/" % str(profile_owner.id))))
@login_required
@multilanguage
def profile_show(request,id):
    class R():
        def __init__(self,claim,requester,request):
            self.claim = claim
            self.requester = requester
            self.request = request
    lang=select_language(request)
    user = request.user.username
    try:
        profile_owner = Person.objects.get(id=id)
    except Person.DoesNotExist:
        add_error(u"Пользователь с id %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    who_can_see=[]
    who_can_see.extend(admins)
    who_can_see.append(profile_owner.login)
    # добавить людей, которые отправляли запрос на предоставление
    # контактных данных
    # получаем список всех тех запросов, которые он отправил другим
    #  людям
    requests = Requests.objects.filter(person=profile_owner)
    # получаем логины этих людей
    requests_owners = list(set([a.claim_owner.login for a in requests]))
    who_can_see.extend(requests_owners)
    # raise NotImplementedError('a')
    if user not in who_can_see:
        add_error(u"Вы не имеете права просматривать этот профиль!",request)
        return (False,(HttpResponseRedirect("/")))
    # Получение заявок для человека
    old_requests = Requests.objects.filter(claim_owner =
                                           profile_owner).filter(
        seen=True)
    given_requests = []
    for r in old_requests:
        given_requests.append(R(r.claim,r.person,r))

    new_requests = Requests.objects.filter(claim_owner =
                                       profile_owner).filter(seen=False)
    claims_with_requests = []
    for r in new_requests:
        r.seen = True
        r.save()
        claims_with_requests.append(R(r.claim,r.person,r))
    # return (True,('register.html',{'UserCreationFormMY':{}},{'title':'GMAH.RU',},request,app))
    return (True,('profile.html',{},{'title':'GMAH.RU',
                                     'profile_owner':profile_owner,
                                     'user':user,
                                     'claims_with_requests':claims_with_requests,
                                     'given_requests':given_requests},
                  request,app))
@login_required
@multilanguage
def profile_edit(request,id):
    lang=select_language(request)
    user = request.user.username
    try:
        profile_owner = Person.objects.get(id=id)
    except Person.DoesNotExist:
        add_error(u"Пользователь с логином %s не найден!" % user,request)
        return (False,(HttpResponseRedirect("/")))
    who_can_edit=[]
    who_can_edit.extend(admins)
    who_can_edit.append(profile_owner.login)
    if user not in who_can_edit:
        add_error(u"Вы не имеете права редактировать этот профиль!",request)
        return (False,(HttpResponseRedirect("/")))
    if request.method == 'POST':
        # form = UserCreationFormMY(request.POST)
        form = get_localized_form('UserEditForm',app,request)(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # new_user = form.save()
            profile_owner.fio = data['fio']
            profile_owner.tel = data['tel']
            profile_owner.mail = data['mail']
            profile_owner.save()
            return (False,(HttpResponseRedirect("/accounts/profile/show/%s/" % profile_owner.id)))

    return (True,('register.html',{'UserEditForm':{'fio':profile_owner.fio,'mail':profile_owner.mail,'tel':profile_owner.tel}},{'title':'GMAH.RU','target':u'Редактируем профиль %s' % user},request,app))
    # return (True,('profile.html',{},{'title':'GMAH.RU','user':user},request,app))
@login_required
@multilanguage
def claim_send_request(request,id):
    lang=select_language(request)
    user = request.user.username
    try:
        claim = Claim.objects.get(id=id)
    except Person.DoesNotExist:
        add_error(u"Заявка с номером  %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    try:
        user = Person.objects.get(login=user)
    except Person.DoesNotExist:
        add_error(u"Пользователь с логином %s не найден!" % user,request)
        return (False,(HttpResponseRedirect("/")))
    # Добавляем разрешение для хозяина заявки на просмотр профиля пользователя, который хочет контактные данные
    result = add_permission(to=user, for_whom=claim.id)
    if result!='OK':
        add_error(u"Результат попытки - %s" % result,request)
        add_error(u"Не удалось задать разрешения на просмотр вашего профиля для хозяина заявки!",request)
        return (False,(HttpResponseRedirect("/")))
    a = datetime.datetime.now()
    c = make_aware(a,get_current_timezone())
    new_request = Requests(claim = claim,
                            person = user,
                            claim_owner = claim.owner,
                            date = c,
                            seen = False)
    new_request.save()
    return (False,(HttpResponseRedirect("/")))
@login_required
@multilanguage
def claim_accept_request(request,request_id):
    """
    Добавляет для заявки право на просмотра для того, кто отправил
    запрос на зявку
    :param request: страндартный параметр
    :param request_id: id запроса
    :return:
    """
    lang=select_language(request)
    user = request.user.username
    try:
        info_request = Requests.objects.get(id=request_id)
    except Requests.DoesNotExist:
        add_error(u"Запрос с номером  %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    claim = info_request.claim
    # Добавляем разрешение для хозяина заявки на просмотр профиля пользователя, который хочет контактные данные
    result = add_permission(to=claim, for_whom=info_request.person.id)
    if result!='OK':
        add_error(u"Результат попытки - %s" % result,request)
        add_error(u"Не удалось задать разрешения на просмотр ваших "
                  u"данных для заявки %s для пользователя %s!" % (
            claim,info_request.person),
                  request)
        return (False,(HttpResponseRedirect("/accounts/profile/")))
    # a = datetime.datetime.now()
    # c = make_aware(a,get_current_timezone())
    # new_request = Requests(claim = claim,
    #                         person = user,
    #                         claim_owner = claim.owner,
    #                         date = c,
    #                         seen = False)
    # new_request.save()
    return (False,(HttpResponseRedirect("/")))
@login_required
@multilanguage
def claim_withdraw_request(request,request_id):
    """
    Добавляет для заявки право на просмотра для того, кто отправил
    запрос на зявку
    :param request: страндартный параметр
    :param request_id: id запроса
    :return:
    """
    lang=select_language(request)
    user = request.user.username
    try:
        info_request = Requests.objects.get(id=request_id)
    except Requests.DoesNotExist:
        add_error(u"Запрос с номером  %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    claim = info_request.claim
    # Добавляем разрешение для хозяина заявки на просмотр профиля пользователя, который хочет контактные данные
    result = remove_permission(to=claim,
                             for_whom=info_request.person.id)
    if result!='OK':
        add_error(u"Результат попытки - %s" % result,request)
        add_error(u"Не удалось задать разрешения на просмотр ваших "
                  u"данных для заявки %s для пользователя %s!" % (
            claim,info_request.person),
                  request)
        return (False,(HttpResponseRedirect("/accounts/profile/")))
    # удаляем сам запрос
    info_request.delete()
    return (False,(HttpResponseRedirect("/")))
@login_required
@multilanguage
def claim_refuse_request(request,request_id):
    """
    Отказ в предоставлении котакных данных. Удаляет объект
    запроса на просмотр + лишает пользователя возможности
    просмотреть профиль того, кто хотел получить данные
    :param request: страндартный параметр
    :param request_id: id запроса
    :return:
    """
    lang=select_language(request)
    user = request.user.username
    try:
        info_request = Requests.objects.get(id=request_id)
    except Requests.DoesNotExist:
        add_error(u"Запрос с номером  %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    # Получаем номер заявки для которой хотели получить данные
    claim = info_request.claim
    # кто просил данные
    who_want_info = info_request.person
    # и для этой заявки удаляем разершение на просмотр данных
    # профиля того, кто просил данные
    result = remove_permission(to=who_want_info,
                             for_whom=claim.id)
    if result!='OK':
        add_error(u"Результат попытки - %s" % result,request)
        add_error(u"Не удалось удалить разрешение на "
                  u"просмотр профиля пользователя %s, "
                  u"выданный для получения данных к заявки %s "
                  u"для пользователю %s!" % (
            who_want_info, claim,info_request.claim_owner),
                  request)
        return (False,(HttpResponseRedirect("/accounts/profile/")))

    # удаляем сам запрос
    info_request.delete()
    return (False,(HttpResponseRedirect("/")))

def save_file(file_instance,id,request):
    # размеры итогового файла
    h=480
    w=480
    background_color = "green"
    # background_color = "white"
    a = datetime.datetime.now()
    c = make_aware(a,get_current_timezone())
    b = str(c)
    # d1 = is_aware(c)
    # d2 = is_naive(c)
    d = '_'.join((b.split(' ')[0],'_'.join(b.split(' ')[1].split('.')[0].split(':')),b.split(' ')[1].split('.')[1].split('+')[0]))
    instanse = File(file=file_instance,
                    timestamp=c,
                    file_name = str(d),
                    description = 'image for '+str(id),)
    instanse.save()
    path_to_file = instanse.file.path
    add_error(u"Файл сохранён по адресу %s" % path_to_file,request)
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
    return instanse

# @login_required
@multilanguage
@shows_errors
@for_admins
def main(request):
    user = request.user.username
    # who_can_delete=[]
    # who_can_delete.extend(admins)
    # who_can_delete.append(claim_owner)
    # media_dir = MEDIA_ROOT
    if user:
        try:
            user = Person.objects.get(login = user)
        except Person.DoesNotExist:
            add_error(u"Пользователь с логином %s не найден!" % user,request)
            return (False,(HttpResponseRedirect("/error/")))
    claims =  Claim.objects.filter(deleted=False).filter(closed=False)
    requests = ''
    if user:
        requests = len(Requests.objects.filter(claim_owner = user).filter(seen=False))
    return (True,('main.html',{},{'title':'GMAH.RU','claims':claims,'user':user,'requests':requests},request,app))
@multilanguage
@shows_errors
def error_page(request):
    user = request.user.username
    return (True,('error.html',{},{'title':'GMAH.RU',
                               'user':user,},request,app))
@login_required
@multilanguage
def claim_delete(request,id):
    # удалять может только хозяин или админ
    try:
        claim = Claim.objects.get(id=id)
    except Claim.DoesNotExist:
        add_error(u"Заявка с номером %s не найдена!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    # a = str(claim.id)
    claim_owner = claim.owner.login
    who_can_delete=[]
    who_can_delete.extend(admins)
    who_can_delete.append(claim_owner)
    user = request.user.username
    if user not in who_can_delete:
        add_error(u"Вы не имеете права удалить эту заявку!",request)
        return (False,(HttpResponseRedirect("/")))
    files=claim.file.all()
    # raise TabError('before for file in files')
    for file in files:
        try:
        # file = File.objects.get(id=file_id)
        # client = file.for_client.get()
        # raise TabError('file %s' % file.file.delete)
            storage, path = file.file.storage, file.file.path
        # raise TabError('storage:path =  %s:%s' % (storage, path))
            storage.delete(path)
            file.delete()
        except :
            logger.error("Unexpected error:", sys.exc_info()[0])
            add_error(u"Файл %s не удалён!" % file,request)
    claim.delete()

    return (False,(HttpResponseRedirect("/")))

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
                        new_claim.file.add(save_file(request.FILES[filed],new_claim.id,request))
                        new_claim.save()
            return (False,HttpResponseRedirect('/'))
        return (False,HttpResponseRedirect('/'))
    return (True,('claim_add.html',{'NewClaimForm':{}},{'title':'GMAH.RU - добавить заявку',},request,app))
@login_required
@multilanguage
def claim_edit(request,id):
    try:
        claim = Claim.objects.get(id=id)
    except Claim.DoesNotExist:
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
            a = request.FILES
            if request.FILES:
                for filed in ('file','file1','file2','file3'):
                    if filed in request.FILES:
                        print request.FILES[filed]
                        claim.file.add(save_file(request.FILES[filed],claim.id,request))
                        claim.save()
            return (False,HttpResponseRedirect('/claim/show/'+str(id)))
        return (False,HttpResponseRedirect('/claim/edit/'+str(id)))
    # тут надо блокировать возможность загрузить новые картинки, больше чем 4-уже_есть
    files = claim.file.all()
    count_of_files = len(files)
    return (True,('claim_add.html',{'NewClaimForm':{'name':claim.name, 'description':claim.description,
                                                    'count_of_files':count_of_files},
                                    },
                  {'title':'GMAH.RU - добавить заявку','files':files},request,app))
@multilanguage
@shows_errors
def claim_show(request,id):
    lang=select_language(request)
    user = request.user.username
    try:
        user = Person.objects.get(login=user)
    except Person.DoesNotExist:
        add_error(u"Пользователь с логином %s не найден!" % user,request)
        return (False,(HttpResponseRedirect("/")))
    try:
        claim = Claim.objects.get(id=id)
    except Claim.DoesNotExist:
        add_error(u"Заявка с номером %s не найдена!" % id,request)
        # return (False,(HttpResponseRedirect("/assets_by_type/"+type_id+"/")))
        return (False,(HttpResponseRedirect("/")))
    # a = str(claim.id)
    title = u'GMAH.RU - заявка %s' % str(claim.name)
    files=claim.file.all()
    if files:
        first_file = files[0]
        files = files[1:]
    else:
        first_file=''
    # Получаем список тех, кто может просмотреть данные пользователей
    can_see_info =  str(user.id) in claim.acl.split(u';') or \
                    user.login in admins or claim.owner.id == user.id
    return (True,('claim_show.html',{},{'title':title ,
                                        'claim':claim,
                                        'files':files,
                                        'first_file':first_file,
                                        'can_see_info':can_see_info,
                                        },request,app))

@login_required
@multilanguage
def image_delete(request,id):
    # удалять может только хозяин или админ
    try:
        file = File.objects.get(id=id)
    except File.DoesNotExist:
        add_error(u"Файл с номером %s не найден!" % id,request)
        return (False,(HttpResponseRedirect("/")))
    # a = str(claim.id)
    claim = file.for_claim.get()
    claim_id = claim.id

    claim_owner = claim.owner.login
    who_can_delete=[]
    who_can_delete.extend(admins)
    who_can_delete.append(claim_owner)
    user = request.user.username
    if user not in who_can_delete:
        add_error(u"Вы не имеете права удалить эту заявку!",request)
        return (False,(HttpResponseRedirect("/")))

    try:
        storage, path = file.file.storage, file.file.path
        storage.delete(path)
        file.delete()
    except :
        logger.error("Unexpected error:", sys.exc_info()[0])
        add_error(u"Файл %s не удалён!" % file,request)

    return (False,(HttpResponseRedirect("/claim/show/%s/" % claim_id)))
