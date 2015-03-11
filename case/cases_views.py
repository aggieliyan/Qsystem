# coding=utf-8
from django.shortcuts import render_to_response, redirect, RequestContext
from models import testcase, casemodule, category, result

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
		case[m.m_name] = testcase.objects.filter(category = pid, module = m.id)
	return render_to_response("case/case_list.html", {"case":case, "result":newresult, "listid":listid})