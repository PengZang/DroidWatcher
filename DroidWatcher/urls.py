#coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import *
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import urlpatterns
from DroidWatcher.routes.apk import *
urlpatterns=patterns('DroidWatcher.routes',
    (r'^$',TemplateView.as_view(template_name="base.html")),
    (r'^admin/', include(admin.site.urls)),
    (r'^apk/search$','apk.search'),
    (r'^apk/upload$','apk.upload'),
    (r'^apk/select$','apk.select'),
    (r'^apk/record$','apk.record'),
    (r'^apk/process$','apk.process'),
    (r'^apk/query$','apk.query'),
    (r'^report/basic$','report.basic'),
    (r'^report/analysis/$','report.addition'),
    (r'^report/edit$','report.edit'),
    (r'^system/info$','system.info'),
    (r'^system/train$','system.startTrain'),
    (r'^system/editMethod$','system.editMethod'),
#     (r'^socket\.io',include(socketio.sdjango.urls)),
)

urlpatterns+=patterns('',
    url('',include('django_socketio.urls')),
)