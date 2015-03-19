# coding=utf-8
from django.shortcuts import render_to_response, redirect, RequestContext,HttpResponse
from models import testcase, casemodule, category, result
from forms import searchForm
import json
from project.views import isNone

def case_list(request,pid):
	case = {}	
	if request.method == "POST":
		search = searchForm(request.POST)
		if search.is_valid():
			categoryid = search.cleaned_data['categoryid']
			ctestmodule = search.cleaned_data['testmodule']
			cpriority = search.cleaned_data['priority']
			cauthor = search.cleaned_data['author']
			cexecutor = search.cleaned_data['executor']
			cstart_date = search.cleaned_data['start_date']
			cend_date = search.cleaned_data['end_date']
			cexec_status = search.cleaned_data['exec_status']
			ckeyword = search.cleaned_data['keyword']
			print "aa"
			# try:
			# 	if not isNone(categoryid):
			# 		print "1"
			# 		cmodule = cmodule.objects.filter(category = categoryid)
			# 		print "2"
			# 	else:
			# 		cmodule = cmodule.objects.filter(category = 0)
			# 	print cmodule					
			# 	if not isNone(cauthor):
			# 		cmodule = cmodule.filter(author = cauthor.strip())
			# 	if not isNone(cpriority):
			# 		cmodule = cmodule.filter(priority = cpriority)
			# 	if not isNone(keyword):
			# 		cmodule = cmodule.filter(action__search = keyword)
			# 	testmodule = casemodule.objects.filter(pk__in = cmodule)
			# 	casereslut = result.objects.filter(testcase__in = cmodule)
			# 	if not isNone(testmodule):
			# 		testmodule = testmodule.filter(m_name = testmodule)
			# 		print testmodule
			# 	if not isNone(cexecutor):
			# 		casereslut = casereslut.filter(executor = cexecutor)
			# 	if not isNone(start_date) and not isNone(end_date):
			# 		casereslut = casereslut.filter(exec_date__range=(start_date, end_date))
			# 	print "3"
			# except Exception:
			# 	pass
			if not isNone(categoryid):
				cmodule = testcase.objects.filter(category = categoryid)
			else:
				cmodule = testcase.objects.filter(category = 0)					
			if not isNone(cauthor):
				cmodule = cmodule.filter(author = cauthor)
			if not isNone(cpriority):
				cmodule = cmodule.filter(priority = cpriority)
			if not isNone(ckeyword):
				cmodule = cmodule.filter(action__search = ckeyword)
			testmodule = casemodule.objects.filter(pk__in = cmodule.values_list("module",flat=True))
			casereslut = result.objects.filter(testcase__in = cmodule)
			if not isNone(ctestmodule):
				testmodule = testmodule.filter(m_name = ctestmodule)
			if not isNone(cexecutor):
				casereslut = casereslut.filter(executor = cexecutor)
			if not isNone(cstart_date) and not isNone(cend_date):
				casereslut = casereslut.filter(exec_date__range = (cstart_date, cend_date))
			print "3"
	else:
		cmodule = testcase.objects.filter(category = pid)
		testmodule = casemodule.objects.filter(pk__in = cmodule.values_list("module", flat = True))
		casereslut = result.objects.filter(testcase__in = cmodule)
	listid = casereslut.values_list("testcase", flat=True).distinct()
	newresult = []
	for c in listid:
		p = casereslut.filter(testcase = c).order_by("-exec_date")[0]
		newresult.append(p)
	for m in testmodule:
		print m.id
		case[m.m_name] = cmodule.filter(module = m.id)
	print case
	return render_to_response("case/case_list.html", {"case":case, "result":newresult, "listid":listid})

def categorysearch(request):
	clist = []
	#一级
	master = category.objects.filter(parent_id__isnull=True)
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