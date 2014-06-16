from django.conf.urls import patterns, url
from project import views

urlpatterns = patterns('',
	url(r'^$', views.new_project, name='new_project'),
	

)