#coding=utf-8
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls import *
# from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.conf.urls.i18n import urlpatterns
from DroidWatcher.routes.apk import *
from account.decorators import login_required
from django.shortcuts import render_to_response
urlpatterns=patterns('DroidWatcher.routes',
#     (r'^$',TemplateView.as_view(template_name="base.html")),
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

@login_required
def home(request):
    return render_to_response('base.html')

urlpatterns+=patterns('',
#     (r'^admin',include(admin.site.urls)),
#     (r'^accounts/',include('DroidWatcher.accounts.urls')),
      url('^$', home, name='home'),
      (r'^account/',include("account.urls")),  
      (r'^test',TemplateView.as_view(template_name="test.html")),
)