# coding=utf-8
from django import forms
from models import Upload

class searchForm(forms.Form):
	cate1 = forms.CharField(required=False)
	cate2 = forms.CharField(required=False)
	cate3 = forms.CharField(required=False)
	categoryid = forms.CharField(max_length=100, required=False)
	testmodule = forms.CharField(required=False)
	priority = forms.CharField(required=False)
	status = forms.CharField(required=False)
	mold = forms.CharField(required=False)
	author = forms.CharField(required=False)
	executor = forms.CharField(required=False)
	start_date = forms.DateField(required=False)
	end_date = forms.DateField(required=False)
	exec_status = forms.CharField(required=False)
	keyword = forms.CharField(required=False)
	
class add_procateForm(forms.Form):
	procate_id = forms.IntegerField(required=False)
	project_id = forms.IntegerField(required=False)
	procate_level = forms.IntegerField(required=False)
	procate_title = forms.CharField(required=True,error_messages={'required': u'产品模块名称不能为空'})
	
class edit_procateForm(forms.Form):
	procate_id1 = forms.IntegerField(required=False)
	procate_title1 = forms.CharField(required=True,error_messages={'required': u'产品模块名称不能为空'})
	project_id1 = forms.IntegerField(required=False)
	
class del_procateForm(forms.Form):
	procate_id_del = forms.IntegerField(required=False)	

class UploadForm(forms.Form):
	Filedata = forms.FileField()
	uptime = forms.DateField(required=False)

	# def handle_uploaded_file(f):
	# 	destination = open('some/file/name.txt', 'wb+')
	# 	for chunk in f.chunks():
	# 		destination.write(chunk)
	# 	destination.close()