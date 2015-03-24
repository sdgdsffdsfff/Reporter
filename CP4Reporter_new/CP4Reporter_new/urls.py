# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
from MainReport import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'CP4Reporter_new.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^syncdb/$',views.sync_CP4_db),
    url(r'^mainreport/$',views.index),
    url(r'^projects/$',views.get_projects_by_product),
    url(r'^issues/$',views.get_issues_by_project),
)
