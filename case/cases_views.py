# coding=utf-8
import datetime
import json, re, xlrd, os, sys
from django.shortcuts import render_to_response, redirect, RequestContext, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from models import testcase, casemodule, category, Upload, result
from forms import searchForm, UploadForm
from project.models import user, department
from project.views import isNone
from django.db.models import Q
from Qsystem import settings
import time

#判断是否是技术部分的测试或者开发
def is_dev(uid):
	depid = user.objects.get(id=int(uid)).department_id
	if depid not in [1, 2, 4, 5, 13]:
		return False
	else:
		return True

#判断是否是测试部门的
def is_tester(uid):
	depid = user.objects.get(id=int(uid)).department_id
	if depid != 1:
		return False
	else:
		return True

def has_children(request):
	resp = {}
	pid = request.GET['pid']
	child = category.objects.filter(parent_id = int(pid))
	try:
		if len(child):	
			resp["haschildren"] = True
		else:
			resp["haschildren"] = False
		resp["success"] = True

	except Exception, e:
		resp["success"] = False
		print e
	finally:
		resp = json.dumps(resp)
		return HttpResponse(resp)

def case_list(request,pid):
	#没登陆的提示去登录
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/case/login")
	#权限判断
	canope = True
	child = category.objects.filter(parent_id = int(pid))
	notice = ''
	if not is_tester(request.session['id']):
		canope =  False
	else:
		if len(child):
			canope =  False
	#列表页显示		
	kwargs={}
	case = []
	cate1 = cate2 = cate3 = categoryid = ctestmodule = 	cpriority = cauthor = \
	cexecutor = cstart_date = cend_date = cexec_status = ckeyword =  cstatue = cmold =  ''
	if request.method == "POST":
		search = searchForm(request.POST)
		if search.is_valid():
			cate1 = search.cleaned_data['cate1']
			cate2 = search.cleaned_data['cate2']
			cate3 = search.cleaned_data['cate3']
			categoryid = search.cleaned_data['categoryid']
			ctestmodule = search.cleaned_data['testmodule']
			cpriority = search.cleaned_data['priority']
			cstatue = search.cleaned_data['status']
			cmold =  search.cleaned_data['mold']
			cauthor = search.cleaned_data['author']
			cexecutor = search.cleaned_data['executor']
			cstart_date = search.cleaned_data['start_date']
			cend_date = search.cleaned_data['end_date']
			cexec_status = search.cleaned_data['exec_status']
			ckeyword = search.cleaned_data['keyword']
			subset2 = list(category.objects.filter(parent_id = pid).values_list("id",flat=True))
			subset3 = list(category.objects.filter(parent_id__in = subset2))
			subset = list(set(subset2).union(set(subset3)))
			subset.append(pid)
			print 'get alltestcase---start', time.ctime()
			cmodule = testcase.objects.filter(category__in = subset, isactived = 1)
			print 'get alltestcase---end', time.ctime()
			
			if ctestmodule or cpriority or cauthor or cexecutor or cstart_date or cend_date or \
			cexec_status or ckeyword or cstatue:
			    canope =  False
			else:
				if len(child):
					cmodule = cmodule.order_by("-id").values_list("pk", flat = True)[:200]
					cmodule = testcase.objects.filter(pk__in = list(cmodule))
					notice = u"类目包含子类目时，当前类目下最多只显示200条哈，请使用筛选项查看更多用例~~"
			# if not isNone(pid):
			# 	kwargs['category__in'] = subset				
			if not isNone(cauthor):
				kwargs['authorid'] = cauthor
			if not isNone(cpriority):
				kwargs['priority'] = cpriority
			if not isNone(ckeyword):
				kwargs['action__contains'] = ckeyword.strip()
			cmodule = cmodule.filter(**kwargs)
			mcase = testcase.objects.filter(category__in = subset)
			allmodule = casemodule.objects.filter(pk__in = mcase.values_list("module",flat=True))
			testmodule = casemodule.objects.filter(pk__in = cmodule.values_list("module",flat=True))		
			rresult = caseresult = result.objects.filter(testcase__in = cmodule)
			allexecutor = result.objects.filter(testcase__in = mcase).values_list("executor",flat = True).distinct()
			if not isNone(ctestmodule):
				testmodule = testmodule.filter(m_name = ctestmodule)
				cmodule = cmodule.filter(module_id__in = testmodule, isactived = 1)
			#等于 、不等于某个状态
			args = [Q(result = cmold) , ~Q(result = cmold)] 
			#不等于(未执行)、等于 1 /0
			args2 = [~Q(pk__in = caseresult.values_list("testcase", flat=True).distinct()),Q(pk__in = caseresult.values_list("testcase", flat=True).distinct())]
			if not isNone(cmold) and not isNone(cstatue):
				if cmold == u"未执行":
					cmodule = cmodule.filter(args2[int(cstatue)])
				else:
					if not cstart_date and not cend_date or cstatue =="1":
						#根据testcase_id进行分组查询，取最新执行状态
						rlist = result.objects.raw('SELECT * FROM (SELECT * FROM case_result ORDER BY exec_date DESC) case_result GROUP BY testcase_id')
						rid = []
						for r in rlist:
							rid.append(r.id)						
						if cstatue == "1":
							cm1 = cmodule.values_list("pk",flat=True)	
							cm2 = rresult.filter(result = cmold,pk__in = rid).values_list("testcase_id",flat=True).distinct()
							idd = set(cm1)^(set(cm2))
							cmodule = cmodule.filter(pk__in = idd , isactived = 1)
						else:
							caseresult = caseresult.filter(args[int(cstatue)], Q(pk__in = rid))
							cmodule = cmodule.filter(pk__in = caseresult.values_list("testcase", flat=True).distinct(),isactived =1)
					else:
						caseresult = caseresult.filter(args[int(cstatue)])
						cmodule = cmodule.filter(pk__in = caseresult.values_list("testcase", flat=True).distinct() , isactived = 1)
			if not isNone(cexecutor):
				caseresult = caseresult.filter(executor = cexecutor)
				cmodule = cmodule.filter(pk__in = caseresult.values_list("testcase", flat=True).distinct() , isactived =1)
			if not isNone(cstart_date) or not isNone(cend_date):
				if not isNone(cstart_date):
					caseresult = caseresult.filter(exec_date__gte = cstart_date)
				if not isNone(cend_date):
					tomorrow = cend_date + datetime.timedelta(days=1)
					caseresult = caseresult.filter(exec_date__lte = tomorrow)
				cdate = set(cmodule.values_list("id",flat = True))&(set(caseresult.values_list("testcase", flat=True)))
				cmodule = cmodule.filter(pk__in = cdate,isactived = 1)
	else:
		try:
			clist = []
			first = get_object_or_404(category, pk=int(pid))
			clist.append(int(pid))
			if first.parent_id != 0:
				clist.append(first.parent_id)
				second = get_object_or_404(category, pk= first.parent_id)
				if second.parent_id !=0:
					clist.append(second.parent_id)
			catelen = len(clist)
			if catelen:
				cate1 = clist[-1]
				catelen = catelen - 1;
			if catelen:
				cate2 = clist[-2]
				catelen = catelen - 1;
			if catelen:
				cate3 = clist[-3]
		except Exception,e:
			pass
		#通过链接访问项目时，没有项目时，返回全部列表页
		ppid = len(category.objects.filter(pk = pid))
		if ppid == 0:
			return HttpResponseRedirect('/case/caselist')
		else:			
			subset2 = list(category.objects.filter(parent_id = pid).values_list("id",flat=True))
			subset3 = list(category.objects.filter(parent_id__in = subset2))
			subset = list(set(subset2).union(set(subset3)))		
			subset.append(pid)
			cmodule = testcase.objects.filter(category__in = subset, isactived = 1)
		if len(child):
			cmodule = cmodule.order_by("-id").values_list("pk", flat = True)[:200]
			cmodule = testcase.objects.filter(pk__in = list(cmodule))
			notice = u"类目包含子类目时，当前类目下最多只显示200条哈，请使用筛选项查看更多用例~~"		
		testmodule = casemodule.objects.filter(pk__in = cmodule.values_list("module", flat = True))
		allmodule = testmodule
		caseresult = result.objects.filter(testcase__in = cmodule)
		allexecutor = caseresult.values_list("executor",flat = True).distinct()
	listid = caseresult.values_list("testcase", flat=True).distinct()
#	print len(listid)
	count = len(cmodule)
#	newresult = []
#	for c in listid:
#		p = caseresult.filter(testcase=c).order_by("-exec_date")[0]
#		newresult.append(p)
	if not ckeyword:
		testmodule = testmodule.order_by("m_rank")
	else:
		testmodule = testmodule.order_by("-id")
	for m in testmodule:
		ccase = {}
		ccase[m.id] = []
		mcaselist = cmodule.filter(module = m.id, isactived = 1).order_by("rank")
		if len(mcaselist) != 0:
			for c in mcaselist:
				try:
					cresult = caseresult.filter(testcase_id = c.id).order_by("-exec_date")[0]
				except:
					cresult = ''
				ccase[m.id].append([c, cresult])
			case.append(ccase)

    #字典进行排序，暂不使用
	# case = sorted(case.iteritems(), key=lambda d:d[1], reverse=False)
	
	print case

	return render_to_response("case/case_list.html", {"case":case, "testmodule":testmodule, "allmodule":allmodule, "count":count,"listid":listid,"categoryid":categoryid, "cauthor":cauthor, 
		                      "cpriority":cpriority, "statue":cstatue, "mold":cmold, "ckeyword":ckeyword, "ctestmodule":ctestmodule, "cexecutor":cexecutor, "cstart_date":cstart_date, 
		                      "cend_date":cend_date, "cate1":cate1, "cate2":cate2, "cate3":cate3, "canope":canope, "allexecutor":allexecutor, "notice":notice})

def allcaselist(request):
	#没登陆的提示去登录
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/case/login")

	kwargs={}
	case = []
	ctestmodule = cpriority = cauthor = cexecutor = cstart_date = cend_date = \
	cexec_status = ckeyword =  cstatue = cmold = notice = ''
	testmodule = casemodule.objects.filter(isactived = 1)
	allmodule = testmodule
	allexecutor = result.objects.all().values_list("executor",flat = True).distinct()
	if request.method == "POST":
		search = searchForm(request.POST)
		if search.is_valid():
			ctestmodule = search.cleaned_data['testmodule']
			cpriority = search.cleaned_data['priority']
			cstatue = search.cleaned_data['status']
			cmold =  search.cleaned_data['mold']
			cauthor = search.cleaned_data['author']
			cexecutor = search.cleaned_data['executor']
			cstart_date = search.cleaned_data['start_date']
			cend_date = search.cleaned_data['end_date']
			cexec_status = search.cleaned_data['exec_status']
			ckeyword = search.cleaned_data['keyword']
			if ctestmodule or cpriority or cauthor or cexecutor or cstart_date or cend_date or \
			cexec_status or ckeyword or cstatue:
				print 'get alltestcase---start1', time.ctime()
				cmodule = testcase.objects.filter(isactived = 1)
				print 'get alltestcase---end1', time.ctime()
			else:
				print 'get alltestcase---start2', time.ctime()
				cmodule = testcase.objects.filter(isactived = 1).order_by("-id").values_list("pk", flat = True)[:200]
				cmodule = testcase.objects.filter(pk__in = list(cmodule))
				notice = u"全部用例下最多只显示200条哈,请使用筛选项查看更多用例~~"
				print 'get alltestcase---end2', time.ctime()
			if not isNone(cauthor):
				kwargs['authorid'] =  cauthor
			if not isNone(cpriority):
				kwargs['priority'] = cpriority
			if not isNone(ckeyword):
				kwargs['action__contains'] = ckeyword.strip()
			print 'get filter---1', time.ctime()
			cmodule = cmodule.filter(**kwargs)
			print 'get filter---2', time.ctime()		
			caseresult = result.objects.filter(testcase__in = cmodule)
			print 'get filter---3', time.ctime()	
			rresult = caseresult
			if not isNone(ctestmodule):
				testmodule = testmodule.filter(m_name = ctestmodule)
				cmodule = cmodule.filter(module_id__in = testmodule, isactived = 1)
			args = [Q(result = cmold) , ~Q(result = cmold)] 
			args2 = [~Q(pk__in = caseresult.values_list("testcase", flat=True).distinct()),Q(pk__in = caseresult.values_list("testcase", flat=True).distinct())]
			if not isNone(cmold) and not isNone(cstatue):
				if cmold == u"未执行":
					cmodule = cmodule.filter(args2[int(cstatue)])
				else:
					if not cstart_date and not cend_date or cstatue =="1":
						#根据testcase_id进行分组查询，取最新执行状态
						rlist = result.objects.raw('SELECT * FROM (SELECT * FROM case_result ORDER BY exec_date DESC) case_result GROUP BY testcase_id')
						rid = []
						for r in rlist:
							rid.append(r.id)						
						if cstatue == "1":
							cm1 = cmodule.values_list("pk",flat=True)	
							cm2 = rresult.filter(result = cmold,pk__in = rid).values_list("testcase_id",flat=True).distinct()
							idd = set(cm1)^(set(cm2))
							cmodule = cmodule.filter(pk__in = idd , isactived = 1)
						else:
							caseresult = caseresult.filter(args[int(cstatue)], Q(pk__in = rid))
							cmodule = cmodule.filter(pk__in = caseresult.values_list("testcase", flat=True).distinct(),isactived =1)
					else:
						caseresult = caseresult.filter(args[int(cstatue)])
						cmodule = cmodule.filter(pk__in = caseresult.values_list("testcase", flat=True).distinct(),isactived =1)
			if not isNone(cexecutor):
				caseresult = caseresult.filter(executor = cexecutor)
				cmodule = cmodule.filter(pk__in = caseresult.values_list("testcase", flat=True).distinct())
			if not isNone(cstart_date) or not isNone(cend_date):
				if not isNone(cstart_date):
					caseresult = caseresult.filter(exec_date__gte = cstart_date)
				if not isNone(cend_date):
					tomorrow = cend_date + datetime.timedelta(days=1)
					caseresult = caseresult.filter(exec_date__lte = tomorrow)
				cdate = set(cmodule.values_list("id",flat = True))&(set(caseresult.values_list("testcase", flat=True)))
				cmodule = cmodule.filter(pk__in = cdate,isactived = 1)
	else:
		cmodule = testcase.objects.filter(isactived = 1).order_by("-id").values_list("pk",flat=True)[:200]
		cmodule = testcase.objects.filter(pk__in = list(cmodule))
		testmodule = testmodule.filter(pk__in = cmodule.values_list("module", flat = True))		
		caseresult = result.objects.filter(testcase__in = cmodule, isactived = 1)
		notice = u"全部用例下最多只显示200条哈,请使用筛选项查看更多用例~~"
	listid = caseresult.values_list("testcase", flat=True).distinct()
	count =len(cmodule)
#	newresult = []
#	for c in listid:
#		p = caseresult.filter(testcase = c).order_by("-exec_date")[0]
#		newresult.append(p)
	if not ckeyword:
		testmodule = testmodule.order_by("m_rank")
	else:
		testmodule = testmodule.order_by("-id")
	for m in testmodule:
		ccase = {}
		ccase[m.id] = []
		mcaselist = cmodule.filter(module = m.id, isactived = 1).order_by("rank")
		if len(mcaselist) != 0:
			for c in mcaselist:
				try:
					cresult = caseresult.filter(testcase_id = c.id).order_by("-exec_date")[0]
				except:
					cresult = ''
				ccase[m.id].append([c, cresult])
			case.append(ccase)
	return render_to_response("case/case_list.html", {"case":case, "testmodule":testmodule, "allmodule":allmodule, "listid":listid, "count":count, "cauthor":cauthor, 
		                      "cpriority":cpriority, "statue":cstatue, "mold":cmold, "ckeyword":ckeyword, "ctestmodule":ctestmodule, "cexecutor":cexecutor, "cstart_date":cstart_date, 
		                      "cend_date":cend_date, "canope": False, "allexecutor":allexecutor, "notice":notice})

def categorysearch(request):
	clist = []
	#一级
	# master = category.objects.filter(parent_id__isnull=True)
	master = category.objects.filter(parent_id = 0, isactived = 1)
	#二级
	for m in master:
		categorydic = {}
		s = {}
		categorydic["master"]=m.name
		categorydic["masterid"] = m.id
		second = category.objects.filter(parent_id = m.id, isactived = 1)
		slist = []
		ms = []
		for s in second:
			msdic = {}					
			msdic["second"] = s.name
			msdic["secondid"] = s.id			
			third = category.objects.filter(parent_id = s.id, isactived = 1)			
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

def exec_log(request,pid):
	clist={}
	record = []
	loglist = result.objects.filter(testcase_id = int(pid))
	execrecord = list(loglist.values_list("result", flat = True))
	clist["Pass"] = execrecord.count("Pass")
	record.append(clist); 
	for item in loglist:
		recorddic = {}
		recorddic["date"] = (item.exec_date).strftime("%Y-%m-%d %H:%M:%S")
		recorddic["executor"] = item.executor
		recorddic["result"] = item.result
		recorddic["remark"] = item.r_remark
		record.append(recorddic)
	return HttpResponse(json.dumps(record))

def execute_case(request):
	resp = {}
	print request.session['id']
	#判断下权限
	if not is_dev(request.session['id']):
		resp["success"] = False
		resp["message"] = "您没有权限执行用例！"
		resp = json.dumps(resp)
		return HttpResponse(resp)

	try:
		caseid = request.POST['caseid']
		cresult = request.POST['cresult']
		executor = request.session['realname']
		executorid = request.session['id']
		exec_date = datetime.datetime.now()
		cr = result(testcase_id=caseid, result=cresult, exec_date=exec_date, executor=executor, executorid=executorid, isactived=1)
		cr.save()
		exedetail = {}
		exedetail['exec_date'] = exec_date.strftime("%Y-%m-%d %H:%M:%S")
		exedetail['executor'] = executor 
		resp["success"] = True
		resp["exedetail"] = exedetail
	except Exception, e:
		resp["success"] = False
		resp["message"] = e
	finally:	
		resp = json.dumps(resp)

		return HttpResponse(resp)


def update_rank(request):
	resp = {}
	#判断下权限
	if not is_tester(request.session['id']):
		resp["success"] = False
		resp["message"] = "对不起，您没有排序的权限~"
		resp = json.dumps(resp)
		return HttpResponse(resp)
	try:
		rank_dict = json.loads(request.POST['rankdict'])
		module_id = request.POST['mid']

		#对字典进行排序
		# rank_list = sorted(rank_dict.items(), key=lambda d: d[1])

		if int(module_id):#更新用例rank
			if int(module_id) != -1:
				m = casemodule.objects.get(id=module_id)
			for key in rank_dict.keys():
				# tc = testcase.objects.get(id=key)
				# if int(module_id) != -1:
				# 	tc.module_id = module_id
				# tc.rank = rank_dict[key]
				# tc.save()
				if int(module_id) != -1:
					testcase.objects.filter(id=key).update(module=m, rank=rank_dict[key])
				else:
					testcase.objects.filter(id=key).update(rank=rank_dict[key])

				
		else:#更新模块rank
			for key in rank_dict.keys():
				# md = casemodule.objects.get(id=key)
				# md.m_rank = rank_dict[key]
				# md.save()
				casemodule.objects.filter(id=key).update(m_rank=rank_dict[key])
			
		resp["success"] = True
	except Exception, e:
		resp["success"] = False
		resp["message"] = e
	finally:
		resp = json.dumps(resp)
		# print "resp==",resp

		return HttpResponse(resp)

def moduledel(request):
	resp = {}
	#判断下权限
	if not is_tester(request.session['id']):
		resp["success"] = False
		resp["message"] = "no permit"
		resp = json.dumps(resp)
		return HttpResponse(resp)

	mid = request.POST['mid']
	try:
		# delmodule = get_object_or_404(casemodule, pk=int(mid))
		# delmodule.isactived = 0
		# delmodule.save()
		casemodule.objects.filter(id=int(mid)).update(isactived=0)
		# delmodule.delete()
		resp["success"] = True
	except Exception,e:
		resp["success"] = False
	finally:
		resp = json.dumps(resp)
		return HttpResponse(resp)

def delete_case(request):

	resp = {}
	#判断下权限
	if not is_tester(request.session['id']):
		resp["success"] = False
		resp["message"] = "对不起,您没有权限删除用例"
		resp = json.dumps(resp)
		return HttpResponse(resp)

	deleteid = request.POST['did']
	deleteid = deleteid.replace(" ", "").split(",")
	while '' in deleteid:
		deleteid.remove('')
	
	try:
		testcase.objects.filter(id__in = deleteid).update(isactived=0)		
		resp["success"] = True
	except Exception, e:
		resp["success"] = False
		resp["message"] = e
	finally:
		resp = json.dumps(resp)
		return HttpResponse(resp)

def update_case_related(request):
	resp = {}
	#判断下权限
	if not is_dev(request.session['id']):
		resp["success"] = False
		resp["message"] = "no permit"
		resp = json.dumps(resp)
		return HttpResponse(resp)
	tname = request.POST['tname']
	tcnt = request.POST['tcnt']
	cid = request.POST['tid']
	print cid
	
	try:
		trs = result.objects.filter(testcase_id=cid).order_by("-id")[0]
		if trs:
			if tname == "wi":
				if len(tcnt) > 8:
					resp['success'] = False
					resp['message'] = "BUG字数不能超过8位"
				trs.wi = tcnt
			else:
				if len(tcnt) > 100:
					resp['success'] = False
					resp['message'] = "备注字数不能超过100位"
				trs.r_remark = tcnt

			trs.save()
			resp["success"] = True
	except Exception, e:
		resp["success"] = False
		print e
	finally:
		resp = json.dumps(resp)
		return HttpResponse(resp)

def savecase(request):
	dict = {}
	#判断下权限
	if not is_tester(request.session['id']):
		dict["message"] = False
		dict = json.dumps(dict)
		return HttpResponse(dict)

	try:
		url = request.META['HTTP_REFERER']
		p = re.compile(r'\d+')
		pid = (p.findall(url))[-1]
		dt = json.loads(request.POST.get('datas',False))
		for data in dt:
			for key,value in data.items():
				for ddata in value:
					if int(key) < 0 or key == 'undefined':
						cm = casemodule(m_name = ddata['mname'],m_rank = ddata['mrank'], isactived = 1)
						cm.save()
						key = cm.id
					else:
						updatemodule = casemodule.objects.filter(pk = key).update(m_name = ddata['mname'])
					caseid = ddata['id']
					if caseid != -3:
						cpre = ddata['precon']
						cinput = ddata['action']
						couput = ddata['output']
						cpriority = ddata['priory']
						crank = ddata['rank']
						if caseid:
							updatecase = testcase.objects.filter(pk = caseid).update(precondition = cpre, \
								action = cinput, output = couput, priority = cpriority)
						else:
							newcase = testcase(category_id = pid, rank = crank, module_id = key, precondition = cpre, \
								action = cinput, output = couput, priority = cpriority, author = request.session['realname'], \
								authorid = request.session['id'], createdate = datetime.datetime.now(), isactived = '1')
							newcase.save()
		dict['message']= True
	except Exception,e: 
		import sys 
		info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
		dict['success']=False
		dict['message']=info
		print e,info
	finally:
		cjson=json.dumps(dict) 
	return HttpResponse(cjson)

def upload_file(request):
	resp = {}
	url = str(request.get_full_path())	
	pid = url.split("/")[-1]
	try:	
		if request.method == 'POST':
			form = UploadForm(request.POST, request.FILES)
			if form.is_valid():
				#获取表单信息
				xlsfile = form.cleaned_data['Filedata']
				filename = xlsfile.name
				print filename
				#写入数据库
				uf = Upload(Filedata = xlsfile, uptime = datetime.datetime.now()) 
				uf.save()
				filepath = uf.Filedata
				uipath = unicode(str(filepath), "utf8")
				uipath = os.path.join(settings.MEDIA_ROOT,uipath)
				excel_table_byindex(request,file= uipath, pid = pid)
				resp['success'] = True
		else:
			form = UploadForm()
	except Exception,e:
		info = "%s" % (sys.exc_info()[1])
		resp['success'] = False
		resp['message'] = info
		# print e, "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
	# finally:
	# 	# resp['snum'] = count[0]
	# 	# resp['fnum'] = count[1]
	# 	print resp
	resp = json.dumps(resp)
	print resp
	return HttpResponse(resp)

def excel_table_byindex(request, file= '',pid = ''):
	data = xlrd.open_workbook(file)
	table = data.sheets()
	key = 0
	crank = 1
	snum = allnum = 0
	count = []		
	for ctable in table:
		nrows = ctable.nrows #行数
		ncols = ctable.ncols #列数
		if nrows >= 7 and ctable.cell(7,0).value == u'结构|用户角色':
			for rownum in range(8,nrows):
				row = ctable.row_values(rownum) 
				if row:
					cpre = row[0].strip()
					cinput = row[1].strip()
					coutput = row[2].strip()
					cpriority = row[3]
					if  cpriority not in [1,2,3]:
						cpriority = 2
					if cpre and  not cinput and not coutput:
						num = len(casemodule.objects.all())
						cm = casemodule(m_name = cpre, m_rank = num, isactived = 1)
						cm.save()
						key = cm.id
						crank = 1
					else:
						allnum = allnum + 1
						if key == 0 :
							key = '';
						if cinput and coutput:				
							newcase = testcase(category_id = int(pid), rank = crank, module_id = int(key), precondition = cpre, \
										action = cinput, output = coutput, priority = cpriority, author = request.POST['realname'], \
										authorid = request.POST['uid'], createdate = datetime.datetime.now(), isactived = '1')
							newcase.save()
							snum = snum + 1;
							crank = crank+1;
	count.append(snum)
	count.append(allnum-snum)
	# return count
