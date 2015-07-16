# coding=utf-8

from django.shortcuts import render_to_response, \
RequestContext, HttpResponseRedirect, HttpResponse
from models import category, testcase, casemodule   
from case.forms import add_procateForm, edit_procateForm, del_procateForm
import datetime
import json
from project.models import user, project_user, project
from django.db.models import Q

def product_category(request):
    try:
        useid = request.session['id']
    except KeyError:
        return HttpResponseRedirect("/case/login")
    #获取登录用户所属部门
    myuser = user.objects.filter(id = useid)
    departid = myuser[0].department_id
    #获取登录用户正在进行中的项目
    my_projects = project_user.objects.filter(username_id = useid)
    if my_projects.count > 0:
        my_proids = []
        for my_project in my_projects:
            my_proids.append(my_project.project_id)
        my_projectlist = project.objects.filter(pk__in = my_proids)
        my_onprojects = my_projectlist.exclude(Q(status_p = u'已上线') | Q(status_p = u'暂停') | Q(status_p = u'运营推广')).order_by("-id")[:6]
        #项目id和产品模块id对应关系
        pro_cate_ids = {}
        if my_onprojects.count > 0:
            for my_onproject in my_onprojects:
                try:
                    my_procate = category.objects.get(project_id = my_onproject.id)
                    pro_cate_ids[my_onproject.id] = my_procate.id  
                except:
                    pro_cate_ids[my_onproject.id] = 0
    #查询出parent_id = 0 的一级产品模块
    first_secounts = {}
    second_thicounts = {}
    second_ids = {}
    second_names = {}
    third_ids = {}
    third_names = {}
    procate_firsts = category.objects.filter(parent_id = '0', isactived = '1')
    fircount = procate_firsts.count()
    # Don't delete. Added by YanLi
    first_level = {}
    second_level = {}
    third_level = {}
    
    if fircount > 0:
        for procate_first in procate_firsts:
            first_level[procate_first.id] = [procate_first.name]
            procate_seconds = category.objects.filter(parent_id = procate_first.id, isactived = '1')
            if procate_seconds.count() > 0:
                first_secounts[procate_first.id] = 1
                for procate_second in procate_seconds:
                    second_ids[procate_second.id] = procate_first.id
                    second_names[procate_second.id] = procate_second.name
                    second_level[procate_second.id] = [procate_first.id, procate_second.name]
                    procate_thirds = category.objects.filter(parent_id = procate_second.id, \
                                                             isactived = '1')
                    if procate_thirds .count() > 0:
                        second_thicounts[procate_second.id] = 1
                        for procate_third in procate_thirds:
                            third_ids[procate_third.id] = procate_second.id
                            third_names[procate_third.id] = procate_third.name 
                            third_level[procate_third.id] = [procate_second.id, procate_third.name]
    if '/getprocate' in request.path:
        res = {'1': first_level, '2': second_level, '3': third_level}
        for num, level in res.items():
            for cate in level:
                level[cate].append({})
                T = testcase.objects.filter(category_id=cate)
                module_ids = T.values('module_id').distinct()
                for item in module_ids:
                    level[cate][-1][item['module_id']] = casemodule.objects.get(id=item['module_id']).m_name        
        return HttpResponse(json.dumps(res))

    return render_to_response("case/product_category.html",RequestContext(request, \
    {'procate_firsts':procate_firsts, 'second_ids':sorted(second_ids.items()), \
     'second_names':second_names.items(), 'third_ids':sorted(third_ids.items()), \
     'third_names':third_names.items(), 'first_secounts':first_secounts.items(), \
     'second_thicounts':second_thicounts.items(), 'my_onprojects':my_onprojects, \
     'departid':departid,'pro_cate_ids':pro_cate_ids.items()}))
    
def add_procate(request, url):
    if request.method == 'POST':
        form = add_procateForm(request.POST)
        if form.is_valid():
            procate_id = form.cleaned_data['procate_id']
            proid = form.cleaned_data['project_id']
            procate_level = form.cleaned_data['procate_level']
            procate_name = form.cleaned_data['procate_title']
            redmine_id = form.cleaned_data['redmine_proid'] 
            if procate_id == None:
                pro_cate = category(name = procate_name, parent_id = 0, project_id = proid, redmine_proid = redmine_id,\
                                    level = 1, createdate = datetime.datetime.now(), isactived = 1)
            else:
                pro_cate = category(name = procate_name, parent_id = procate_id, project_id = proid, \
                                    redmine_proid = redmine_id, level = procate_level + 1, \
                           createdate = datetime.datetime.now(), isactived = 1)
            pro_cate.save()                  
    return HttpResponseRedirect(url)

def edit_procate(request, url):
    if request.method == 'POST':
        form = edit_procateForm(request.POST)
        if form.is_valid():
            procate_id = form.cleaned_data['procate_id1']
            procate_name = form.cleaned_data['procate_title1']
            proid1 = form.cleaned_data['project_id1']
            redmine_id = form.cleaned_data['redmine_proid1']  
            pro_cate = category.objects.get(id = procate_id)
            pro_cate.name = procate_name
            pro_cate.project_id = proid1   
            pro_cate.redmine_proid = redmine_id        
            pro_cate.save()                  
    return HttpResponseRedirect(url)

def delprocate_confirm(request): 
    procate_id = request.GET['procate_id']
    son_category = category.objects.filter(parent_id = procate_id, isactived = 1)   
    son_count = son_category.count()
    testcases = testcase.objects.filter(category_id = procate_id, isactived = 1)
    cast_count = testcases.count()
    if son_count > 0:
        according = "has_son"
    elif cast_count > 0:
        according = "has_case"
    else:
        according = "no"  
    accord = json.dumps(according)
    return HttpResponse(accord)

def get_proid(request): 
    procate_id = request.GET['procate_id']
    pro_cate = category.objects.get(id = procate_id)   
    proid = pro_cate.project_id
    pro_id = json.dumps(proid)
    print pro_id
    return HttpResponse(pro_id)

def get_redmine_proid(request): 
    procate_id = request.GET['procate_id']
    pro_cate = category.objects.get(id = procate_id)   
    redmine_id = pro_cate.redmine_proid
    redmine_proid = json.dumps(redmine_id)
    print redmine_proid
    return HttpResponse(redmine_proid)
      
def del_procate(request, url):
    if request.method == 'POST':
        form = del_procateForm(request.POST)
        if form.is_valid():
            procate_id = form.cleaned_data['procate_id_del']
            pro_cate = category.objects.get(id = procate_id)
            pro_cate.delete()       
    return HttpResponseRedirect(url)

def has_proid(request):
    proid = request.GET['proid']
    procates = category.objects.filter(project_id = proid)
    if procates.count() > 0:
        accordname = procates[0].name + "has" + str(procates[0].id)
    else:
        accordname = "no"
    accord_name = json.dumps(accordname)
    return HttpResponse(accord_name)