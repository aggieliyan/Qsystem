# coding=utf-8
from django.shortcuts import render_to_response, redirect
import models
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse

def case_pull(request):
    return render_to_response("case/case_pull.html")
 
def getcases(request): 
    caselist = models.testcase.objects.all().order_by("-id")
    """分页"""
    paginator = Paginator(caselist, 5)
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
    if caseobj.has_previous():
        previouslink = "/case/getcases/?page=" + str(caseobj.previous_page_number())
    if caseobj.has_next():
        nextlink = "/case/getcases/?page=" + str(caseobj.next_page_number())

    res = {'actionlist': actionlist, 'curpage': pagenum, 'totalpage': paginator.num_pages, 'prelink': previouslink, 'nextlink': nextlink}
    return HttpResponse(json.dumps(res))