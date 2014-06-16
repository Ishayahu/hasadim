from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin

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
)
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
