from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
import project

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Qsystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^newproject/',include('project.urls')),
    url(r'^create/', project.views.create, name='create'),
    url(r'^showperson', project.views.show_person),
    url(r'^projectlist', project.views.project_list),
    url(r'^tongyongtou', project.views.tongyongtou),
    url(r'^psearch', project.views.psearch),
    url(r'^delay', project.views.delay),
)
