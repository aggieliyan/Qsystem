# coding=utf-8
from django import forms

class ProjectForm(forms.Form):
	priority = forms.IntegerField(required=True, error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})
	pname = forms.CharField(required=True, error_messages={'required':u'项目名称不能为空'})
	status = forms.CharField(required=True, error_messages={'required':u'项目状态不能为空'})
	leader = forms.IntegerField(required=True, error_messages={'required':u'负责人不能为空'})
	designer = forms.IntegerField(required=False)
	tester = forms.IntegerField(required=False)
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

class changedesignForm(forms.Form):
	content=forms.CharField(required=True,error_messages={'invalid':u'变更内容不能为空'})
	dpath = forms.CharField(required=True,error_messages={'invalid':u'设计图地址不能为空'})
	changeid = forms.IntegerField(required=True)


class delayprojectForm(forms.Form):
	delay_date=forms.DateField(required=True,error_messages={'invalid':u'延期日期不能为空'})
	delay_reason = forms.CharField(required=True,error_messages={'invalid':u'延期理由不能为空'})
	delayid = forms.IntegerField(required=True)
class ProjectSearchForm(forms.Form):
	project=forms.CharField(required=False)
	start_date_s=forms.DateField(required=False)
	end_date_s=forms.DateField(required=False)
	status_p=forms.CharField(required=False)
	leader_p=forms.CharField(required=False)