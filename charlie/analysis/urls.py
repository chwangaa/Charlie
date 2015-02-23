from django.conf.urls import patterns, url
import views
import ajax

urlpatterns = patterns('',
    url(r'^$','django.contrib.auth.views.login',{
                'template_name': 'landing.html'},name='landing'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^index/$', views.dashboard, name='dashboard'),
    url(r'^(?P<datasource_id>\d+)/download/$', ajax.downloadFile, name='download'),
    url(r'^add_name/$', views.addNameView, name='add_name'),
    url(r'^addDict/$', ajax.addDict, name='addingDict'),    
    url(r'^addName/$', ajax.addName, name='addingName'),    
    url(r'^add_dict/$', views.addDictView, name='add_dict'),
    url(r'^index/delete-datasource/$', ajax.delete_datasource, name='delete_datasource'),
    url(r'^(?P<datasource_id>\d+)/$', views.analysis, name='analysis'),
    url(r'^(?P<datasource_id>\d+)/manip/update/$', ajax.update_manipulated, name='manip_update'),
    url(r'^(?P<datasource_id>\d+)/manip/$', views.dataManipulation, name='manipulation'),
    url(r'^(?P<datasource_id>\d+)/update/$', ajax.update, name='update'),
    url(r'^(?P<datasource_id>\d+)/dele/$', views.delD, name='deleD'),
)