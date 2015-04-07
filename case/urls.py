from django.conf.urls import patterns, url
from case import cases_views, login_views, category_views, casepull_views
from project import views

urlpatterns = patterns('',
	url(r'^login/', views.login, {"url":"../caselist"},name='login'),
	url(r'^logout/', login_views.logout),
	url(r'^caselist/(\d+)/$', cases_views.case_list, name='caselist'),
	url(r'^caselist/', cases_views.allcaselist, name='allcaselist'),
	url(r'^procate/', category_views.product_category, name='procate'),
	url(r'^pull/', casepull_views.case_pull, name='casepull'),
	url(r'^casecate/', cases_views.categorysearch),
)