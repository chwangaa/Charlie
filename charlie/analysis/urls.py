from django.conf.urls import patterns, url
import views
import ajax
import modification_event_handlers as events


urlpatterns = patterns('',
    url(r'^$','django.contrib.auth.views.login',{
                'template_name': 'landing.html'},name='landing'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^index/$', views.dashboard, name='dashboard'),
    url(r'^add_name/$', views.addNameView, name='add_name'),
    url(r'^add_dict/$', views.addDictView, name='add_dict'),
    url(r'^add_skip/$', views.addSkipView, name='add_skip'),
    url(r'^add_typo/$', views.addTypoView, name='add_typo'), 
    url(r'^(?P<datasource_id>\d+)/deleteSMS$', ajax.deleteSMS, name='deleteSMS'),
    url(r'^(?P<datasource_id>\d+)/$', views.analysis, name='analysis'),
    url(r'^(?P<datasource_id>\d+)/manip/$', views.dataManipulation, name='manipulation'),
    url(r'^(?P<datasource_id>\d+)/dele/$', views.delD, name='deleD'),
    url(r'^addDict/$', ajax.addDict, name='addingDict'),
    url(r'^addName/$', ajax.addName, name='addingName'),
    url(r'^delete_word/$', ajax.deleteWord, name='deleteWord'),
    url(r'^index/delete-datasource/$', ajax.delete_datasource, name='delete_datasource'),
    url(r'^(?P<datasource_id>\d+)/download/$', ajax.downloadFile, name='download'),
    url(r'^(?P<datasource_id>\d+)/manip/update/$', ajax.update_manipulated, name='manip_update'),
    url(r'^(?P<datasource_id>\d+)/repName/$', events.replaceNames, name='replaceNames'),
    url(r'^(?P<datasource_id>\d+)/remSkip/$', events.removeSkipWords, name='remSkips'),
    url(r'^(?P<datasource_id>\d+)/remNonAlpha/$', events.removeNonAlphaBetical, name='remNonAlpha'),
    url(r'^(?P<datasource_id>\d+)/repSlang/$', events.replaceSlang, name='repSlang'),

)