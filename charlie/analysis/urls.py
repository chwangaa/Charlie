from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$','django.contrib.auth.views.login',{
                'template_name': 'landing.html'},name='landing'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^index/$', views.dashboard, name='dashboard'),
    url(r'^words/$', views.viewWords, name='word_list'),
    url(r'^add_words/$', views.addName, name='add_name'),
    url(r'^(?P<datasource_id>\d+)/$', views.analysis, name='analysis'),
    url(r'^(?P<datasource_id>\d+)/manip/$', views.dataManipulation, name='manipulation'),
    url(r'^(?P<datasource_id>\d+)/chart/$', views.charts, name='charts'),
    url(r'^(?P<datasource_id>\d+)/update/$', views.update, name='update'),
)