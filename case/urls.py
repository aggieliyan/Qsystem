from django.conf.urls import patterns, url
from case import cases_views, login_views, category_views, casepull_views
from project import views

urlpatterns = patterns('',
	url(r'^login/', views.login, {"url":"../caselist"},name='login'),
	url(r'^logout/', login_views.logout),
	url(r'^caselist/(\d+)/$', cases_views.case_list, name='caselist'),
	url(r'^caselist/', cases_views.allcaselist, name='allcaselist'),
	url(r'^procate/', category_views.product_category, name='procate'),
    url(r'^add_procate/', category_views.add_procate,{'url':'../procate/'},name="add_procate"),
    url(r'^edit_procate/', category_views.edit_procate,{'url':'../procate/'},name="edit_procate"),
	url(r'^delprocate_confirm', category_views.delprocate_confirm),
	url(r'^del_procate/', category_views.del_procate,{'url':'../procate/'},name="del_procate"),
	url(r'^pull/', casepull_views.case_pull, name='casepull'),
	url(r'^casecate/', cases_views.categorysearch),
	url(r'^execlog/(\d+)/$', cases_views.exec_log,name="execlog"),
	url(r'^executecase/', cases_views.execute_case),
	url(r'^updaterank/', cases_views.update_rank),
	url(r'^singledel/(\d+)/$', cases_views.singledel,name='singledel'),
	url(r'^singledel/(\d+)/$', cases_views.singledel,name="\'singledel\'"),
)