# -*- coding:utf-8 -*-
# coding=<utf8>

from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin
from django.contrib.auth.views import login, logout, password_change,password_change_done

import gmah.views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gmah.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


	url(r'^$', gmah.views.main),
	url(r'^claim/add/$', gmah.views.claim_add),
	url(r'^claim/show/(\d+)/$', gmah.views.claim_show),
	url(r'^claim/edit/(\d+)/$', gmah.views.claim_edit),
	url(r'^claim/delete/(\d+)/$', gmah.views.claim_delete),
	url(r'^claim/send_request/(\d+)/$', gmah.views.claim_send_request),
	url(r'^claim/accept_request/(\d+)/$',
        gmah.views.claim_accept_request),
	url(r'^/claim/withdraw_request/(\d+)/$',
        gmah.views.claim_withdraw_request),

	url(r'^image/delete/(\d+)/$', gmah.views.image_delete),

    url(r'^error/', gmah.views.error_page),

# Для администратора:
    url(r'^accounts/$', login),
    url(r'^login/$', login),
    url(r'^accounts/login/$', login),
    url(r'^password_change/$', password_change),
    url(r'^password_change_done/$', password_change_done),
    url(r'^accounts/register/$', gmah.views.register),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/profile/show/(\d+)/$', gmah.views.profile_show),
    url(r'^accounts/profile/edit/(\d+)/$', gmah.views.profile_edit),
    url(r'^accounts/profile/$', gmah.views.profile_redirect),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
