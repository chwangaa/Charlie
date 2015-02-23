# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
	url(r'^analysis/', include('charlie.analysis.urls')),
	url(r'^$', RedirectView.as_view(url='/analysis/')), # Just for ease of use.
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^login/', RedirectView.as_view(url='/analysis/login')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()