from django.conf.urls import patterns, include, url
from project.views import detail
from django.contrib import admin
admin.autodiscover()
import project


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Qsystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^newproject/',include('project.urls')),
    url(r'^showperson', project.views.show_person),
    url(r'^projectlist', project.views.project_list),
    url(r'^psearch', project.views.psearch),
    url(r'^detail/(\d+)/$',detail,name="prodetail"),
    #homepage
    url(r'^personal_homepage/$', project.views.personal_homepage,name="homepage"),
    url(r'^changedesign/', project.views.changedesign,name="design_change"),
    url(r'^delayproject/$', project.views.delayproject,name="project_delay"),
    url(r'^pauseproject-(?P<id>\d+)/$', project.views.pauseproject,name="project_pause"),
    url(r'^deleteproject-(?P<id>\d+)/$', project.views.deleteproject,name="project_delete"),
    
    #sourcemanage
    url(r'^sourcemanage/$',views.show_user),
    url(r'^show_user/$',views.show_user),
    url(r'^nopermit/$',views.nopermit),
    url(r'^show_user2/$',views.show_user2),
    url(r'^Insert_user1/$',views.Insert_user1),
    url(r'^Insert_user2/$',views.Insert_user2),
    url(r'^Insert_user3/$',views.Insert_user3),
    url(r'^delete_user1/$',views.delete_user1),
    url(r'^delete_user2/$',views.delete_user2),
    url(r'^delete_user3/$',views.delete_user3),
    url(r'^delet_userlogic/$',views.delet_userlogic),
    url(r'^delet_userlogic2/$',views.delet_userlogic2),
    url(r'^delet_userlogic3/$',views.delet_userlogic3),

)
