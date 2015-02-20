from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$','django.contrib.auth.views.login',{
                'template_name': 'landing.html'},name='landing'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^index/$', views.dashboard, name='dashboard'),
    url(r'^words/$', views.viewWords, name='word_list'),
    url(r'^add_name/$', views.addNameView, name='add_name'),
    url(r'^addDict/$', views.addDict, name='addingDict'),    
    url(r'^addName/$', views.addName, name='addingName'),    
    url(r'^add_dict/$', views.addDictView, name='add_dict'),
    url(r'^index/delete-datasource/$', views.delete_datasource, name='delete_datasource'),
    url(r'^(?P<datasource_id>\d+)/$', views.analysis, name='analysis'),
    url(r'^(?P<datasource_id>\d+)/manip/update/$', views.update_manipulated, name='manip_update'),
    url(r'^(?P<datasource_id>\d+)/manip/$', views.dataManipulation, name='manipulation'),
    url(r'^(?P<datasource_id>\d+)/chart/$', views.charts, name='charts'),
    url(r'^(?P<datasource_id>\d+)/update/$', views.update, name='update'),
)