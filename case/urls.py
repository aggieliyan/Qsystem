from django.conf.urls import patterns, url
from case import cases_views, login_views, category_views, casepull_views
from project import views

urlpatterns = patterns('',
	url(r'^login/', views.login, {"url":"../procate"},name='login'),
	url(r'^logout/', login_views.logout),
	url(r'^caselist/(\d+)/$', cases_views.case_list, name='caselist'),
	url(r'^caselist/(\d+)/$', cases_views.case_list, name='\'caselist\''),
	url(r'^caselist/$', cases_views.allcaselist, name='allcaselist'),
	url(r'^procate/', category_views.product_category, name='procate'),
    url(r'^add_procate/', category_views.add_procate,{'url':'../procate/'},name="add_procate"),
    url(r'^edit_procate/', category_views.edit_procate,{'url':'../procate/'},name="edit_procate"),
	url(r'^delprocate_confirm', category_views.delprocate_confirm),
	url(r'^get_proid', category_views.get_proid),
	url(r'^has_proid', category_views.has_proid),
	url(r'^del_procate/', category_views.del_procate,{'url':'../procate/'},name="del_procate"),
	url(r'^pull/', casepull_views.case_pull, name='casepull'),
	url(r'^casecate/', cases_views.categorysearch),
	url(r'^getcases/', casepull_views.getcases),
	url(r'^totalpage/', casepull_views.getcases),
	url(r'^getprocate/', category_views.product_category),
	url(r'^execlog/(\d+)/$', cases_views.exec_log,name="execlog"),
	url(r'^executecase/', cases_views.execute_case),
	url(r'^updaterank/', cases_views.update_rank),
	url(r'^moduledel/', cases_views.moduledel, name= 'moduledel'),
	url(r'^savecase/', cases_views.savecase),
	url(r'^deletecase/', cases_views.delete_case),
	url(r'^updateresult/', cases_views.update_case_related),
	url(r'^haschildren/', cases_views.has_children),
	url(r'^upload/', cases_views.upload_file),
)