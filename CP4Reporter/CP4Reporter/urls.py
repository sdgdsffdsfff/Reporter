from django.conf.urls import patterns, include, url
from django.contrib import admin
from HomePage import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.index,name='index'),
    url(r'^ajaxSendMail/$',views.send_email),
    url(r'^mainreport/$',views.mainReport),
    url(r'^getEveryData/$',views.getEveryData),
    url(r'^syncCP4DB/$',views.syncCP4DB),
    url(r'^syncdb/$',views.syncDb),
    #url(r'^personal/\?(\w+)\=(.+)',views.personalPage),
    url(r'^personalBug/',views.personalBugPage),
    url(r'^projectBug/',views.projectBugPage),
    url(r'^allBug/$',views.allBugPage),
    url(r'^allPro/$',views.getProjectPage),
    url(r'^bugDetails/',views.bugDetails),
    url(r'^todayBugDetails/',views.todayBugDetails),
    url(r'^personalBugDetails/',views.personalBugDetails),
    url(r'^chart/$',views.getChart),
)
