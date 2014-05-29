# coding=utf-8
from django.shortcuts import render_to_response, redirect, render
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.template import RequestContext
import forms
import models
import json
from django.db import connection
import MySQLdb
from django.contrib.sessions.models import Session
import datetime
# Create your views here.
def new_project(request):
 
    return render_to_response('newproject.html', locals())

def project_list(request):
    return render_to_response('page.html', locals())

def tongyongtou(request):
	return render_to_response('tongyongtou.html', locals())
    
def detail(request, pid):
    pro = models.project.objects.get(id=int(pid))
    user = models.user.objects.get(id = pro.leader_p_id)
    date =[pro.estimated_product_end_date, pro.estimated_product_start_date, pro.estimated_develop_end_date, pro.estimated_develop_start_date, pro.estimated_test_end_date, pro.estimated_test_start_date]
 
    dt = {'ptime':pro.estimated_product_end_date - pro.estimated_product_start_date, 'dtime': pro.estimated_develop_end_date - pro.estimated_develop_start_date, 'ttime': pro.estimated_test_end_date - pro.estimated_test_start_date}
    res = {'pro':pro, 'user':user, 'dt': dt}

    return render_to_response('detail.html',{'res': res})
                              
def create(request):
	if request.method == 'POST':
		form = forms.ProjectForm(request.POST)
		if form.is_valid():
			priority = form.cleaned_data['priority']
			pname = form.cleaned_data['pname']
			status = form.cleaned_data['status']
			leader = form.cleaned_data['leader']
			leader = models.user.objects.get(id=leader)
			sdate = form.cleaned_data['startdate']
			pdate = form.cleaned_data['plandate']
			psdate = form.cleaned_data['psdate']
			pedate = form.cleaned_data['pedate']
			dsdate = form.cleaned_data['dsdate']
			dedate = form.cleaned_data['dedate']
			tsdate = form.cleaned_data['tsdate']
			tedate = form.cleaned_data['tedate']
			ppath = form.cleaned_data['ppath']
			dppath = form.cleaned_data['dppath']
			tppath = form.cleaned_data['tppath']
			tcpath = form.cleaned_data['tcpath']
			trpath = form.cleaned_data['trpath']
			relateduser = form.cleaned_data['relateduser']
			pro = models.project(priority=priority, project=pname, status_p=status, leader_p =leader, start_date=sdate, expect_launch_date=pdate, real_launch_date=tsdate, estimated_product_start_date=psdate, estimated_product_end_date=pedate, estimated_develop_start_date=dsdate, estimated_develop_end_date=dedate, estimated_test_start_date=tsdate, estimated_test_end_date=tedate, blueprint_p=ppath, develop_plan_p=dppath, test_plan_p=tppath, test_case_p=tcpath, test_report_p=trpath, isactived=1)
			pro.save()

			#存完项目，存相关产品测试开发人员信息
			relateduser = relateduser.replace(" ","").split(",")
			print relateduser
			if len(relateduser):
				pid = models.project.objects.get(project=pname).id
				for uid in relateduser:
					if uid:
						project_user = models.project_user(username_id=uid, project_id=pid,isactived=1)
						project_user.save()
						print 'ok'
			return redirect('/projectlist/')

	else:
	    form = forms.ProjectForm()
	return render(request, 'newproject.html', {'form':form})
	#return render_to_response('page.html', context_instance=RequestContext(request))

def show_person(request):
	roles = request.GET['role']
	key = 0
	if roles == "tes":
		key = 1
	elif roles == "dev":
		key = 2
	elif roles == "pro":
		key = 3
	else:
		key = 0
	person = models.user.objects.filter(department_id = key)
	rs=[]
	if len(person) == 0:
		return HttpResponse(rs, mimetype='application/javascript')
	for item in person:
		uid = item.id
		realname = item.realname
		dic = {'id':int(uid), 'realname':realname}
		rs.append(dic)
	rrs = {"person":rs}
	rs = json.dumps(rrs)
	#return HttpResponse(rs, mimetype='application/javascript')
	return HttpResponse(rs)

