from django.conf.urls import patterns, url
from project import views

urlpatterns = patterns('',
	url(r'^$', views.new_project, name='new_project'),
	url(r'^create/', views.create, name='create'),
	#url(r'^create/', views.create, name='create'),
	#url(r'^showperson', views.show_person),
)