from django.conf.urls import patterns, include, url
from project.views import detail, new_project, register, project_feedback, feedback_comment
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
    url('^cron/$','project.cron.my_scheduled_job'), #for testing timing task~
    #login    
    url('^$', 'project.views.project_list',name="index"),
    url('^login', 'project.views.login',name="login"),
#    url('^register', 'project.views.register',name="register"),i
    ('^register/$',register),
    ('^register/([^/]+)/$',register),
    url('^logout','project.views.logout'),
    url('^nologin','project.views.no_login'),
    url('^noperm/', 'project.views.no_perm'),
    url(r'^initdata/', project.views.initdata),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newproject//$', new_project),
    url(r'^newproject/$', new_project),
    url(r'^newproject/(\d+)/$', new_project),
    url(r'^newproject/(\d+)/(\d+)$', new_project),
    url(r'^projectlist/', project.views.project_list),
    url(r'^psearch', project.views.psearch),
    url(r'^detail/(\d+)/$', project.views.detail,name="prodetail"),
    url(r'^detail/(\d+)/$', project.views.detail, name="\'prodetail\'"),
    url(r'^detail/(\d+)/#feedback', project.views.detail,name="feedback"),
    url(r'^detail/(\d+)/#feedback', project.views.detail, name="\'feedback\'"),
    url(r'^user_info', project.views.user_info),
    #homepage url added 'p' is projectlist's url
    url(r'^personal_homepage/$', project.views.personal_homepage,name="homepage"),
    url(r'^changedesign/', project.views.changedesign,{'url':'../personal_homepage/'},name="design_change"),
    url(r'^pchangedesign/', project.views.changedesign,{'url':'../projectlist/'},name="pdesign_change"),
    url(r'^delayproject/$', project.views.delayproject,{'url':'../personal_homepage/'},name="project_delay"),
    url(r'^pdelayproject/$', project.views.delayproject,{'url':'../projectlist/'},name="pproject_delay"),
    url(r'^pauseproject-(?P<pid>\d+)/$', project.views.pauseproject,{'url':'../personal_homepage/'},name="project_pause"),
    url(r'^pauseproject-(?P<pid>\d+)/$', project.views.pauseproject,{'url':'../personal_homepage/'},name="\'project_pause\'"),
    url(r'^ppauseproject-(?P<pid>\d+)/$', project.views.pauseproject,{'url':'../projectlist/'},name="pproject_pause"),
    url(r'^ppauseproject-(?P<pid>\d+)/$', project.views.pauseproject,{'url':'../projectlist/'},name="\'pproject_pause\'"),
    url(r'^deleteproject-(?P<pid>\d+)/$', project.views.deleteproject,{'url':'../personal_homepage/'},name="project_delete"),
    url(r'^deleteproject-(?P<pid>\d+)/$', project.views.deleteproject,{'url':'../personal_homepage/'},name="\'project_delete\'"),
    url(r'^pdeleteproject-(?P<pid>\d+)/$', project.views.deleteproject,{'url':'../projectlist/'},name="pproject_delete"),
    url(r'^pdeleteproject-(?P<pid>\d+)/$', project.views.deleteproject,{'url':'../projectlist/'},name="\'pproject_delete\'"),
    url(r'^praise/(\d+)/$', project.views.praise,name="praise"),
    url(r'^praise/(\d+)/$', project.views.praise,name="\'praise\'"),
   #sourcemanage
    url(r'^judge/$',project.views.judge),
    url(r'^sourcemanage/$',project.views.show_user),
    url(r'^show_user/$',project.views.show_user),
    url(r'^show_source/$',project.views.show_source),
    url(r'^show_user2/$',project.views.show_user2),
    url(r'^Insert_user/(\d+)/(\d+)/(\d+)/$',project.views.Insert_user),
    ('^detail/(\d+)/$',detail),
    ('^feedback/$', project_feedback),
    ('^comment/$', feedback_comment),
    url(r'^editproject/(\d+)/$', detail, name="editproject"),
    url(r'^editproject/(\d+)/$', detail, name="\'editproject\'"),
    url(r'^editproject/(\d+)/(\d+)$', detail,name="similarpro"),
    url(r'^editproject/(\d+)/(\d+)$', detail,name="\'similarpro\'"),
    url(r'^delay',project.views.delay),
    url(r'^notice',project.views.notice),
    url(r'^historymessage',project.views.historymessage),
    url(r'^refuse',project.views.refuse),
    url(r'^deletehistory',project.views.deletehistory),
    url(r'^confirmmessage',project.views.confirmmessage),
    url(r'^emptyehistory',project.views.emptyehistory),
    url(r'^deletenotice',project.views.deletenotice),
    url(r'^approve',project.views.approve),
    #statistics_list
    url(r'^sdetail',project.views.statistics_detail),
    url(r'^statistics_operate', project.views.statistics_operate,name="addoperate'"),
    url(r'^statistics_operate', project.views.statistics_operate,name="\'addoperate\'"),
    url(r'^sflip/(\d+)/$', project.views.sdropdown),

    #statistics
    url(r'^slist/$', project.views.show_slist),
    url(r'^getsdata/(\d+)/$', project.views.sdata),
)
from django.conf import settings 
if settings.DEBUG is False:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,
        }),
   )
# else:
#     import debug_toolbar
#     urlpatterns += patterns('',
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     )
