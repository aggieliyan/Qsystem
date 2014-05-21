# coding=utf-8
from django import forms

class ProjectForm(forms.Form):
	priority = forms.IntegerField(required=True, error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})
	pname = forms.CharField(required=True, error_messages={'required':u'项目名称不能为空'})
	status = forms.CharField(required=True, error_messages={'required':u'项目状态不能为空'})
	leader = forms.IntegerField(required=True, error_messages={'required':u'负责人不能为空'})
	startdate = forms.DateField(required=False)
	plandate=forms.DateField(required=False)
	psdate = forms.DateField(required=False)
	pedate = forms.DateField(required=False)
	dsdate = forms.DateField(required=False)
	dedate = forms.DateField(required=False)
	tsdate = forms.DateField(required=False)
	tedate = forms.DateField(required=False)
	ppath = forms.CharField(required=False)
	dppath = forms.CharField(required=False)
	tppath = forms.CharField(required=False)
	tcpath = forms.CharField(required=False)
	trpath = forms.CharField(required=False)
	relateduser = forms.CharField(required=False)