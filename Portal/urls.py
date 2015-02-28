from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Zinc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'Portal.views.home', name='home'),
    url(r'^loop/', 'Portal.views.loop', name='home'),
    url(r'^loop_zip/', 'Portal.views.loop_zip', name='home'),
    url(r'^baidu/', 'Portal.views.baidu', name='home'),
)
