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
    skey = request.GET.get('skey')     #如果这三个为空，则给它们赋以空字符，方便后面返回链接时字符串的联结
    if mid:
        caselist = models.testcase.objects.filter(module_id=mid)
    elif cids:
        mid = ''        
        cid = cids.split(',')
        text = ''
        k = 0
        for i in cid:
            if i!= '':                                
                if k==0:
                    text += 'Q(category_id=' + i + ')'
                    k = 1
                else:
                    text += '| Q(category_id=' + i + ')'          
        caselist = models.testcase.objects.filter(eval(text))          
    else:
        mid = ''
        cids = ''
        caselist = models.testcase.objects.all()
    if skey:
        caselist = caselist.filter(action__contains=skey) 
    else:
        skey = ''
    caselist = caselist.filter(isactived=1).order_by("rank")

    """分页"""
    paginator = Paginator(caselist, 25)
   
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
    actionlist  = []
    for case in caseobj:
        cases = {}
        cases[case.id] = case.action
        actionlist.append(cases)
    previouslink = False
    nextlink = False
    if caseobj.has_previous():
        previouslink = "/case/getcases/?page=" + str(caseobj.previous_page_number()) \
                +"&mid="+mid+"&cids="+cids+"&skey="+skey
    if caseobj.has_next():
        nextlink = "/case/getcases/?page=" + str(caseobj.next_page_number()) \
            + "&mid=" + mid + "&cids=" + cids + "&skey=" + skey
    go_link = "/case/getcases/?mid=" + mid + "&cids=" + cids + "&skey=" + skey \
            + "&page="
    
    res = {'actionlist': actionlist, 'prelink': previouslink, 'nextlink': nextlink, 'golink': go_link, 'totalpage': paginator.num_pages}
    return HttpResponse(json.dumps(res))