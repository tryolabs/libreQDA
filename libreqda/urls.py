from django.contrib import admin
from django.conf.urls import patterns, include, url

admin.autodiscover()

urlpatterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # projects
    url(r'^$',
        'libreqda.views.home',
        name='home'),
    url(r'^project/$',
        'libreqda.views.browse_projects',
        name='browse_projects'),
    url(r'^project/new/$',
        'libreqda.views.new_project',
        name='new_project'),
    url(r'^project/(?P<pid>\d+)/delete/$',
        'libreqda.views.delete_project',
        name='delete_project'),
    url(r'^project/(?P<pid>\d+)/copy/$',
        'libreqda.views.copy_project',
        name='copy_project'),
    # accounts
    url(r'^accounts/login/$',
        'django.contrib.auth.views.login',
        name='login'),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout',
        name='logout',
        kwargs={'next_page': '/accounts/login'}),
)
