from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^entershifts/$', views.entershifts, name='entershifts'),
    url(r'^(?P<userpk>[0-9]+)/showreport/(?P<year>[0-9]+)/(?P<month>[0-9]+)$', views.showreport, name='showreport'),
    url(r'^addreport/$', views.addreport, name='addreport'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]