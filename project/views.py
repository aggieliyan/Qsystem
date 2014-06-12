# coding=utf-8
from django.shortcuts import render_to_response, redirect, render,get_object_or_404
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import RequestContext
import forms
import models
import json
from django.db import connection
import MySQLdb
from django.contrib.sessions.models import Session
import datetime
from django.core.urlresolvers import reverse
from django.db.models import Q
from project.models import *

# Create your views here.
def new_project(request):
	form = forms.ProjectForm()
	if request.method == 'POST':
		form = forms.ProjectForm(request.POST)
		if form.is_valid():
			priority = form.cleaned_data['priority']
			pname = form.cleaned_data['pname']
			status = form.cleaned_data['status']
			leader = form.cleaned_data['leader']
			leader = models.user.objects.get(id=leader)
			designer = form.cleaned_data['designer']
			designer  = models.user.objects.get(id=designer )
			tester = form.cleaned_data['tester']
			tester  = models.user.objects.get(id=tester )
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
			pro = models.project(priority=priority, project=pname, status_p=status, leader_p =leader, designer_p=designer,tester_p=tester, start_date=sdate, expect_launch_date=pdate, real_launch_date=tsdate, estimated_product_start_date=psdate, estimated_product_end_date=pedate, estimated_develop_start_date=dsdate, estimated_develop_end_date=dedate, estimated_test_start_date=tsdate, estimated_test_end_date=tedate, blueprint_p=ppath, develop_plan_p=dppath, test_plan_p=tppath, test_case_p=tcpath, test_report_p=trpath, isactived=1)
			pro.save()

			#存完项目，存相关产品测试开发人员信息
			relateduser = relateduser.replace(" ","").split(",")
			print relateduser
			if len(relateduser):
				pid = models.project.objects.filter(project=pname)[0].id
				for uid in relateduser:
					if uid:
						project_user = models.project_user(username_id=uid, project_id=pid,isactived=1)
						project_user.save()
			return redirect('/projectlist/')

	return render(request, 'newproject.html', {'form':form})
 
def project_list(request):
    return render_to_response('page.html', locals())
    
def detail(request, pid):
    pro = models.project.objects.get(id=int(pid))
    user = models.user.objects.get(id = pro.leader_p_id)
    date =[pro.estimated_product_end_date, pro.estimated_product_start_date, pro.estimated_develop_end_date, pro.estimated_develop_start_date, pro.estimated_test_end_date, pro.estimated_test_start_date]
 
    dt = {'ptime':pro.estimated_product_end_date - pro.estimated_product_start_date, 'dtime': pro.estimated_develop_end_date - pro.estimated_develop_start_date, 'ttime': pro.estimated_test_end_date - pro.estimated_test_start_date}
    res = {'pro':pro, 'user':user, 'dt': dt}

    return render_to_response('detail.html',{'res': res})
                              

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
	num = len(person) 
	if num == 0:
		rrs = {"person":rs}
		rs = json.dumps(rrs)
		return HttpResponse(rs)
	for item in person:
		uid = item.id
		realname = item.realname
		dic = {'id':int(uid), 'realname':realname}
		rs.append(dic)
	rrs = {"person":rs}
	rs = json.dumps(rrs)
	return HttpResponse(rs)

def psearch(request):
	key = request.GET['key']
	prs = models.user.objects.filter(realname__contains=key)
	rs = []
	if len(prs) > 0:
		for item in prs:
			dic = {'id':item.id, 'realname':item.realname}
			rs.append(dic)
		rrs = {"person":rs}
		rs = json.dumps(rrs)
	return HttpResponse(rs)

#homepage部分views
def personal_homepage(request):
    result=project.objects.exclude(Q(status_p=u'已上线')| Q(status_p=u'暂停'))
    result1=project.objects.exclude(~Q(status_p=u'已上线')& ~Q(status_p=u'暂停'))
    puser=project_user.objects.all()
    return render_to_response('personal_homepage.html',
        {'result':result,'result1':result1,'puser':puser})

def deleteproject(request,id):
    delpro=get_object_or_404(project,pk=int(id))    
    delpro.delete()
    return HttpResponseRedirect(reverse("homepage"))


def pauseproject(request,id):
    pausepro=get_object_or_404(project,pk=int(id))
    pausepro.status_p='暂停'
    pausepro.save()
    return HttpResponseRedirect(reverse("homepage"))

def delayproject(request):
    if request.method=='POST':
        form = delayprojectForm(request.POST)
        if form.is_valid():
            delayid=form.cleaned_data['delayid']
            delay_date = form.cleaned_data['delay_date']
            delay_reason = form.cleaned_data['delay_reason']
            delpro=project.objects.get(id=delayid)
            uid=delpro.leader_p
            protitle=delpro.project
            delay_p=project_delay(application=uid,project_id=delayid,delay_to_date=delay_date,apply_date=datetime.datetime.now(),title=protitle,reason=delay_reason,result="jieshou",review_date=datetime.datetime.now(),isactived="1")
            delay_p.save()                   
    return HttpResponseRedirect(reverse("homepage"))


def changedesign(request):    
          
    if request.method=='POST':
        form = changedesignForm(request.POST)
        if form.is_valid():
            changeid=form.cleaned_data['changeid']
            content = form.cleaned_data['content']
            dpath = form.cleaned_data['dpath']
            chd=project.objects.get(id=changeid)
            uid=chd.leader_p
            chd.blueprint_p=dpath
            chd.save()
            pub_message=public_message(project_id=changeid,publisher=uid,content=content,type_p="message",publication_date=datetime.datetime.now(),isactived="1")
            pub_message.save()           
    return HttpResponseRedirect(reverse("homepage"))

