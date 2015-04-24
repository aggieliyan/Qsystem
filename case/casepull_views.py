# coding=utf-8
from django.shortcuts import render_to_response, redirect
import models
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.db.models import Q

def case_pull(request):
    case_ids = request.GET.get('cases')
    case_ids = case_ids.split(',')
    case_infos = []
    for i in case_ids:
        if i:
            a = models.testcase.objects.get(id=i)
            case_infos.append([a.precondition, a.action, a.output])
    
    return HttpResponse(json.dumps(case_infos))
 
def getcases(request): 
    #如果选择了模块，则不用管分类，直接筛模块即可，没有模块再筛末级分类
    mid = request.GET.get('mid')
    cids = request.GET.get('cids')
    skey = request.GET.get('skey')
    if mid:
        caselist = models.testcase.objects.filter(module_id=mid)
    elif cids:         
        cids = cids.split(',')
        text = ''
        k = 0
        for i in cids:
            if k==0:
                text += 'Q(category_id=' + i + ')'
                k = 1
            else:
                text += '| Q(category_id=' + i + ')'            
        caselist = models.testcase.objects.filter(eval(text))           
    else:
        caselist = models.testcase.objects.all().order_by("-id")
    if skey:
        caselist = caselist.filter(action__contains=skey) 

    """分页"""
    paginator = Paginator(caselist, 25)
    if '/totalpage' in request.path:
        res = {'totalpage': paginator.num_pages}
        return HttpResponse(json.dumps(res))
   
    pagenum = request.GET.get('page')
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    try:
        caseobj = paginator.page(pagenum)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        caseobj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        caseobj = paginator.page(paginator.num_pages)
    actionlist  = {}
    for case in caseobj:
        actionlist[case.id] = case.action
    
    previouslink = False
    nextlink = False
    if mid or cids or skey:
        if caseobj.has_previous():
            previouslink = "/case/getcases/?page=" + str(caseobj.previous_page_number()) \
                +"&mid="+mid+"&cids="+cids+"&skey="+skey
        if caseobj.has_next():
            nextlink = "/case/getcases/?page=" + str(caseobj.next_page_number()) \
                + "&mid=" + mid + "&cids=" + cids + "&skey=" + skey
        go_link = "/case/getcases/?mid=" + mid + "&cids=" + cids + "&skey=" + skey \
            + "&page="
    else:        
        if caseobj.has_previous():
            previouslink = "/case/getcases/?page=" + str(caseobj.previous_page_number())
        if caseobj.has_next():
            nextlink = "/case/getcases/?page=" + str(caseobj.next_page_number())
        go_link = ""

    res = {'actionlist': actionlist, 'prelink': previouslink, 'nextlink': nextlink, 'golink': go_link}
    return HttpResponse(json.dumps(res))