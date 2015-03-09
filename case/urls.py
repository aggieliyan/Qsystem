from django.conf.urls import patterns, url
from case import cases_views, login_views, category_views, casepull_views

urlpatterns = patterns('',
	url(r'^login/', login_views.login, name='login'),
	url(r'^caselist/', cases_views.case_list, name='caselist'),
	url(r'^procate/', category_views.product_category, name='procate'),
	url(r'^pull/', casepull_views.case_pull, name='casepull'),
)