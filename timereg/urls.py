from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^entershifts/$', views.entershifts, name='entershifts'),
    url(r'^showreport/(?P<year>[0-9]+)/(?P<month>[0-9]+)$', views.showreport, name='showreport'),
    url(r'^addreport/$', views.addreport, name='addreport'),
    url(r'^listreports/$', views.list_reports, name='listreports'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]