from django.conf.urls import patterns, include, url
from project.views import detail, new_project
from django.contrib import admin
admin.autodiscover()
import project

#login
from django.views.generic import TemplateView
#login

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Qsystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
   
    #login
    url('^$', 'project.views.project_list',name="index"),
    url('^login', 'project.views.login',name="login"),
    url('^register', 'project.views.register',name="register"),
    url('^logout','project.views.logout'),
    url('^nologin','project.views.no_login'),
    url('^noperm/', 'project.views.no_perm'),
    url(r'^initdata/', project.views.initdata),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newproject//$', new_project),
    url(r'^newproject/$', new_project),
    url(r'^newproject/(\d+)/$', new_project),
    url(r'^newproject/(\d+)/(\d+)$', new_project),
       
   # url(r'^create/(\d*)', project.views.create, name='create'),
    url(r'^showperson', project.views.show_person),
    url(r'^projectlist/', project.views.project_list),
    url(r'^psearch', project.views.psearch),
    url(r'^detail/(\d+)/$', project.views.detail,name="prodetail"),
    url(r'^detail/(\d+)/$', project.views.detail, name="\'prodetail\'"),
    url(r'^showuser', project.views.show_headname),
    #homepage url added 'p' is projectlist's url
    url(r'^personal_homepage/$', project.views.personal_homepage,name="homepage"),
    url(r'^changedesign/', project.views.changedesign,{'url':'../personal_homepage/'},name="design_change"),
    url(r'^pchangedesign/', project.views.changedesign,{'url':'../projectlist/'},name="pdesign_change"),
    url(r'^delayproject/$', project.views.delayproject,{'url':'../personal_homepage/'},name="project_delay"),
    url(r'^pdelayproject/$', project.views.delayproject,{'url':'../projectlist/'},name="pproject_delay"),
    url(r'^pauseproject-(?P<id>\d+)/$', project.views.pauseproject,{'url':'../personal_homepage/'},name="project_pause"),
    url(r'^pauseproject-(?P<id>\d+)/$', project.views.pauseproject,{'url':'../personal_homepage/'},name="\'project_pause\'"),
    url(r'^ppauseproject-(?P<id>\d+)/$', project.views.pauseproject,{'url':'../projectlist/'},name="pproject_pause"),
    url(r'^ppauseproject-(?P<id>\d+)/$', project.views.pauseproject,{'url':'../projectlist/'},name="\'pproject_pause\'"),
    url(r'^deleteproject-(?P<id>\d+)/$', project.views.deleteproject,{'url':'../personal_homepage/'},name="project_delete"),
    url(r'^deleteproject-(?P<id>\d+)/$', project.views.deleteproject,{'url':'../personal_homepage/'},name="\'project_delete\'"),
    url(r'^pdeleteproject-(?P<id>\d+)/$', project.views.deleteproject,{'url':'../projectlist/'},name="pproject_delete"),
    url(r'^pdeleteproject-(?P<id>\d+)/$', project.views.deleteproject,{'url':'../personal_homepage/'},name="\'pproject_delete\'"),
   #sourcemanage
    url(r'^judge/$',project.views.judge),
    url(r'^sourcemanage/$',project.views.show_user),
    url(r'^show_user/$',project.views.show_user),
    url(r'^show_source/$',project.views.show_source),
    url(r'^show_user2/$',project.views.show_user2),
    url(r'^Insert_user/(\d+)/(\d+)/(\d+)/$',project.views.Insert_user),
    ('^detail/(\d+)/$',detail),
    url(r'^editproject/(\d+)/$', detail, name="editproject"),
    url(r'^editproject/(\d+)/$', detail, name="\'editproject\'"),
    url(r'^editproject/(\d+)/(\d+)$', detail),
    url(r'^delay',project.views.delay),
    url(r'^notice',project.views.notice),
    url(r'^historymessage',project.views.historymessage),
    url(r'^refuse',project.views.refuse),
    url(r'^deletehistory',project.views.deletehistory),
    url(r'^emptyehistory',project.views.emptyehistory),
    url(r'^deletenotice',project.views.deletenotice),
    url(r'^approve',project.views.approve),
)
from django.conf import settings 
if settings.DEBUG is False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,
        }),
   )
