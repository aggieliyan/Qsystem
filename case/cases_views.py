# coding=utf-8
from django.shortcuts import render_to_response, redirect, RequestContext,HttpResponse
from models import testcase, casemodule, category, result
import json

def case_list(request,pid):
	case = {}
	cmodule = testcase.objects.filter(category = pid)
	testmodule = casemodule.objects.filter(pk__in = cmodule)
	casereslut = result.objects.filter(testcase__in = cmodule)
	listid = casereslut.values_list("testcase", flat=True).distinct()
	newresult = []
	for c in listid:
		p = casereslut.filter(testcase = c).order_by("-exec_date")[0]
		newresult.append(p)
	for m in testmodule:
		case[m.m_name] = cmodule.filter(module = m.id)
	return render_to_response("case/case_list.html", {"case":case, "result":newresult, "listid":listid})

def categorysearch(request):
	clist = []
	#一级
	master = category.objects.filter(parent_id = 0)
	#二级
	for m in master:
		categorydic = {}
		s = {}
		categorydic["master"]=m.name
		categorydic["masterid"] = m.id
		second = category.objects.filter(parent_id = m.id)
		slist = []
		ms = []
		for s in second:
			msdic = {}					
			msdic["second"] = s.name
			msdic["secondid"] = s.id			
			third = category.objects.filter(parent_id = s.id)			
			td = []
			for t in third:
				thirdic = {}			
				thirdic["third"]=t.name
				thirdic["thirdid"] = t.id
				td.append(thirdic)
			msdic["thirdlist"]=td
			ms.append(msdic)
		categorydic["slist"]=ms
		clist.append(categorydic)
	# print clist
	return HttpResponse(json.dumps(clist))