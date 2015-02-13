from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
	url(r'^$', views.landing, name='landing'),
    url(r'^index/$', views.dashboard, name='dashboard'),
    url(r'^(?P<datasource_id>\d+)/$', views.analysis, name='analysis'),
    url(r'^(?P<datasource_id>\d+)/chart/$', views.charts, name='charts'),
)