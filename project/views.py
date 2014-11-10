# coding=utf-8
from django.shortcuts import render_to_response, redirect, get_object_or_404, RequestContext
#from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
import json
import time
from django.contrib.sessions.models import Session
import datetime
from django.db.models import Q
from project.forms import UserForm, LoginForm, ProjectForm, changedesignForm, delayprojectForm, TestForm, Approveform, LoginForm, MessageForm, NoticeForm, ProjectSearchForm ,ConmessageForm
from models import department, project, project_user, public_message, project_delay, project_user_message , project_operator_bussniess_message
import models
import hashlib
import django.contrib.auth.models
from django.views.decorators.csrf import csrf_exempt
from models import project, user, project_user, project_delay, public_message, project_user_message, project_statistics
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import ugettext_lazy as _
#test
from django.contrib.auth.models import User, Group
from django.contrib import auth

from django.db import connections
import datetime

def register(request,uname=''):
    if uname =='':      #若是直接Q系统注册为空,以ldap第一次登录则会传来用户名
        if request.method == "POST":
            uf = UserForm(request.POST)
            if uf.is_valid():
                #返回注册成功页面
                #往Django user表里再插入一条数据
                username = uf.cleaned_data['username']
                password = uf.cleaned_data['password']
                realname = uf.cleaned_data['realname']
                email = username+"@ablesky.com"
                try:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                except:
                    uf = UserForm()
                    return render_to_response('register.html', {'list':department.objects.all(),
                                                                'error':'注册的用户名已存在'},
                                              context_instance=RequestContext(request))
                user_new = uf.save()
    
                #如果是产品部门，加入产品部门权限组
                depid = uf.cleaned_data['departmentid']
                if depid == '3':
                    User.objects.get(username=username).groups.add(3)
    
                #登录
                uid = models.user.objects.filter(username=username)[0].id
                request.session['username'] = username
                request.session['realname'] = realname
                request.session['id'] = uid
    
                #Django 认证系统的登录
                user = auth.authenticate(username=username, password=password)
                auth.login(request, user)
    
                return HttpResponseRedirect("/personal_homepage")
        else:
            uf = UserForm()
    
        return render_to_response('register.html', {'list':department.objects.all()},
                                  context_instance=RequestContext(request))
    else:
        if request.method == "POST":
            uf = UserForm(request.POST)
            if uf.is_valid():
                #返回注册成功页面
                #往Django user表里再插入一条数据
                username = uf.cleaned_data['username']
                password = uf.cleaned_data['password']
                realname = uf.cleaned_data['realname']
                email = username+"@ablesky.com"    
                #如果是产品部门，加入产品部门权限组
                depid = int(uf.cleaned_data['departmentid'])
                if depid == 3:
                    User.objects.get(username=username).groups.add(3)
                uid = models.user.objects.filter(username=username)[0].id
                u = models.user(id=uid, username=username,
                                       realname=realname,
                                       password=password,
                                       create_time=datetime.datetime.now(),
                                       department=department.objects.get(id=depid),
                                       isactived=1)
                u.save()
                request.session['username'] = username
                request.session['realname'] = realname
                request.session['id'] = uid
    
                #Django 认证系统的登录
                user = auth.authenticate(username=username, password=models.user.objects.filter(username=username)[0].password)
                auth.login(request, user)
    
                return HttpResponseRedirect("/personal_homepage")
        
        userinfo = models.user.objects.filter(username=uname)[0]
        return render_to_response('register.html', {'list':department.objects.all(),
                                                    'info': userinfo})

def logout(request):
    try:

        response = HttpResponseRedirect("/login")
        response.delete_cookie("username")
        response.delete_cookie("password")

        session_key = request.session.session_key
        Session.objects.get(session_key=session_key).delete()

        #认证系统的退出
        #auth.logout()
        return response
    except:
        pass
    return HttpResponseRedirect("/login/")

def no_login(request):
    return render_to_response("nologin.html")

def no_perm(request):
    return render_to_response("noperm.html")
def login(request):
    template_var = {}
    if "username" in request.COOKIES and "password" in request.COOKIES:
        username = request.COOKIES["username"]
        password = request.COOKIES["password"]
        _userset = models.user.objects.filter(username__exact=username, password__exact=password)
        if _userset.count() >= 1:
            _user = _userset[0]
            request.session['username'] = username
            request.session['realname'] = realname
        return HttpResponseRedirect("/personal_homepage")
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = hashlib.md5(form.cleaned_data["password"]).hexdigest()
            isautologin = form.cleaned_data["isautologin"]
            try:                
                user = auth.authenticate(username=username, password=form.cleaned_data["password"]) #先去ldap验证,如果没有再去django的User表里验证,一旦验证成功,返回用户名,不成功,返回None
                if user != None:                   
                    isldap = models.user.objects.filter(username__exact=username)
                    if len(isldap) == 0: #说明该用户通过ldap第一次登录,数据库尚未存储该用户
                        newUser = User.objects.filter(username=username)[0]       #django User表
                        newuser = models.user(username=username, password='1234', realname=newUser.first_name, create_time=datetime.datetime.now(), department_id='100', isactived=1)
                        newuser.save()
                        newUser.password = '81dc9bdb52d04dc20036dbd8313ed055'       #设置django的User表密码为1234,否则注册后登录无法通过authenticate()验证.
                        newUser.save()
                        link = str("/register/" + username)
                        return HttpResponseRedirect(link)
                    
                    _userset = models.user.objects.filter(username__exact=username)    
                    if _userset.count() >= 1:
                        _user = _userset[0]
                        if _user.isactived:
                            request.session['username'] = _user.username
                            request.session['realname'] = _user.realname
                            request.session['id'] = _user.id
                            auth.login(request, user)
                        else:
                            template_var["error"] = _(u'您输入的帐号未激活，请联系管理员') 
                            template_var["form"] = form
                            return render_to_response("login.html", template_var, context_instance=RequestContext(request))  
                else:
                    template_var["error"] = _(u'您输入的帐号或密码有误，请重新输入')  
                    template_var["form"] = form
                    return render_to_response("login.html", template_var, context_instance=RequestContext(request))                          
            except:
                template_var["error"] = _(u'您输入的帐号或密码有误，请重新输入')
                template_var["form"] = form
                return render_to_response("login.html", template_var, context_instance=RequestContext(request))    
            
            response = HttpResponseRedirect("/personal_homepage")           
            if isautologin:
                response.set_cookie("username", username, 3600)
                response.set_cookie("password", password, 3600)   
            return response
        
    template_var["form"] = form
    return render_to_response("login.html", template_var, context_instance=RequestContext(request))  

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

def new_project(request, pid='', nid=''):
    #没登陆的提示去登录
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/nologin")
    #编辑的得有编辑权限
    if pid:
        uid = request.session['id']
        cpro = models.project.objects.get(id=pid)
        #如果是负责人且有编辑权限才可以
        flag = 0
        mid = [cpro.leader_p_id, cpro.designer_p_id, cpro.tester_p_id, cpro.business_man_id, cpro.operator_p_id, cpro.customer_service_id]
        if uid in mid or request.user.has_perm('auth.change_permission'):
            if request.user.has_perm('project.change_project'):
                flag = 1

        if not flag:
            return HttpResponseRedirect("/noperm")

    #新建的得有新建权限
    if not pid and not request.user.has_perm('project.add_project'):
        return HttpResponseRedirect("/noperm")

    if request.user.has_perm('auth.change_permission'):
        editdate = 1
    else:
        editdate = 0
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            type_p = form.cleaned_data['type_p']
            priority = form.cleaned_data['priority']
            pname = form.cleaned_data['pname']
            description = form.cleaned_data['description']
            status = form.cleaned_data['status']
            leaderid = form.cleaned_data['leader']
            leader = models.user.objects.get(id=leaderid)
            designer = form.cleaned_data['designer']
            tester = form.cleaned_data['tester']
            business_man = form.cleaned_data['business_man']
            operator_p = form.cleaned_data['operator_p']
            customer_service = form.cleaned_data['customer_service']
            roles = [designer, tester, business_man, operator_p, customer_service]
            for i in range(len(roles)):
                if roles[i]:
                    roles[i] = models.user.objects.get(id=roles[i])
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
            relateduser0 = form.cleaned_data['relateduser0']
            relateduser1 = form.cleaned_data['relateduser1']
            relateduser2 = form.cleaned_data['relateduser2']
            relateduser3 = form.cleaned_data['relateduser3']
            relateduser4 = form.cleaned_data['relateduser4']
            relateduser5 = form.cleaned_data['relateduser5']
            countsql = form.cleaned_data['countsql']
            countsql = strQ2B(countsql)
            remark_p = form.cleaned_data['remark_p']

            if pid == '' or nid == '1':
                pro = models.project(type_p=type_p, priority=priority, \
                    project=pname, description=description, \
                    status_p=status, leader_p=leader, \
                    designer_p=roles[0], tester_p=roles[1], start_date=sdate, \
                    business_man =roles[2], operator_p = roles[3],\
                    customer_service = roles[4],\
                    expect_launch_date=pdate, \
                    estimated_product_start_date=psdate, \
                    estimated_product_end_date=pedate, \
                    estimated_develop_start_date=dsdate, \
                    estimated_develop_end_date=dedate, \
                    estimated_test_start_date=tsdate, \
                    estimated_test_end_date=tedate, blueprint_p=ppath, \
                    develop_plan_p=dppath, test_plan_p=tppath, \
                    test_case_p=tcpath, test_report_p=trpath, \
                    remark_p =remark_p, isactived=1)
            else:
                rdate = models.project.objects.get(id=pid).real_launch_date
                pnum = models.project.objects.get(id=pid).praise_p
                pro = models.project(id=pid, type_p=type_p, \
                    priority=priority,project=pname, \
                    description=description, \
                    status_p=status, leader_p=leader, \
                    designer_p=roles[0], tester_p=roles[1], \
                    business_man = roles[2], \
                    operator_p = roles[3],\
                    customer_service = roles[4],\
                    start_date=sdate, \
                    expect_launch_date=pdate, \
                    real_launch_date=rdate, \
                    estimated_product_start_date=psdate, \
                    estimated_product_end_date=pedate, \
                    estimated_develop_start_date=dsdate, \
                    estimated_develop_end_date=dedate, \
                    estimated_test_start_date=tsdate, \
                    estimated_test_end_date=tedate, blueprint_p=ppath, \
                    develop_plan_p=dppath, test_plan_p=tppath, \
                    test_case_p=tcpath, test_report_p=trpath, \
                    remark_p=remark_p,isactived=1, praise_p=pnum)
            pro.save()
            #存完项目，存相关产品测试开发等人员信息
            
            #如果是新建就取出刚才存在的项目id,否则是编辑则删掉此前的用户与项目的关系
            if pid == '' or nid =='1':
                pid = models.project.objects.filter\
                (project=pname).order_by("-id")[0].id
            else:
                models.project_user.objects.filter(project_id=pid).delete()

            relateduser = [relateduser0, relateduser1, relateduser2, relateduser3, relateduser4, relateduser5]
            for i in range(len(relateduser)):
                #把相关人员的id存入列表中
                relateduser[i] = relateduser[i].replace(" ", "").split(",")
                if len(relateduser[i]):          
                    #存用户与项目的关系
                    for uid in relateduser[i]:
                        if uid:
                            #Django bulk_create
                            project_user = models.project_user\
                            (username_id=uid, project_id=pid, roles=i, isactived=1)
                            project_user.save()

            #存完人员,存统计查询语句
            psql = countsql.split(";")
            if pid == '' or nid =='1':
                pid = models.project.objects.filter\
                    (project=pname).order_by("-id")[0].id
            else:
                models.project_statistics.objects.filter(project_id=pid).delete()
            for sql in psql:
                if ":" in sql:
                    item = sql.split(":")[0]
                    db = sql.split(":")[1]
                    sql = sql.split(":")[2]
                    project_statistics = models.project_statistics(
                                        project_id=pid, item=item, db=db, sql=sql)
                    project_statistics.save()
            
            musername = models.user.objects.get(id=leaderid).username
            #给项目负责人加入到项目负责人权限组
            User.objects.get(username=musername).groups.add(4)

            #给其他负责人加入到相应负责人权限组
            allmasters = [[designer, 5], [tester, 6], [business_man, 7], [operator_p, 8], [customer_service, 9]]
            for m in allmasters:
                if m[0]:
                    print m[0]
                    mname = models.user.objects.get(id=m[0]).username
                    print "mmmmmmmmmmmmmmmmm"
                    print mname
                    User.objects.get(username=mname).groups.add(m[1])
            # if designer:
            #     dusername = models.user.objects.get\
            #     (id=form.cleaned_data['designer']).username
            #     #给产品负责人加入到产品负责人权限组
            #     User.objects.get(username=dusername).groups.add(5)
            # if tester:
            #     tusername = models.user.objects.get\
            #     (id=form.cleaned_data['tester']).username
            #     #给测试负责人加入到测试负责人权限组
            #     User.objects.get(username=tusername).groups.add(6)



            #项目设计完成需要给业务负责人和产品负责人发消息，project_operator_bussniess_message和public_message
            #project_user_message这三个表
            #设计完成isactived存2，测试中isactived存3，上线给留言发消息isactived存1，上线发公告isactived存0
            #--杜
            if status == u"设计完成":
                flag = 0
                prolist = public_message.objects.filter\
                (project=pid).filter(isactived=2).order_by("-id")
                try:
                    prolist[0].isactived
                except IndexError:
                    try:
                        request.session['id']
                    except KeyError:
                        return HttpResponseRedirect("/nologin")
                    else:
                        flag = 1                        
                else:
                    if prolist[0].isactived != 2:
                        try:
                            request.session['id']
                        except KeyError:
                            return HttpResponseRedirect("/nologin")
                        else:
                            flag = 1
                if flag == 1:        
                    usrid = request.session['id']
                    project = models.project.objects.get(id=pid)
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                    content = project.project + u"于"+time+u"设计完成，请立即查看设计图并确认！"    
                    uids = []
                    if project.business_man_id > 0 :
                        uids.append(project.business_man_id)
                    if project.operator_p_id > 0 :
                        uids.append(project.operator_p_id)
                    if project.customer_service_id > 0 :
                        uids.append(project.customer_service_id)
                    for uid in uids :
                        #存表public_message
                        pmessage = public_message(project=pid, \
                                              publisher=uid, content=content, type_p="message", \
                                              publication_date=datetime.datetime.now(), \
                                              delay_status = "未确认" ,\
                                              isactived=2)
                        pmessage.save()
                        #存表project_user_message
                        #存该项目的业务负责人、客服负责人和运营负责人，只有这三个个人哦 
                        messageid = public_message.objects.filter(publisher = uid).order_by("-id")[0]
                        ppmessage = project_user_message(userid_id = uid , messageid_id = messageid.id ,\
                                                        project_id = pid , isactived = True )
                        ppmessage.save()
                    #存表project_operator_bussniess_message
                    #存该项目的业务负责人、客服负责人和运营负责人，只有这三个个人哦
                    if project.business_man_id > 0 :
                        pmessage = project_operator_bussniess_message(userid_id=project.business_man_id , project_id = pid ,\
                                                                  user_type = "业务" ,\
                                                                  title = "设计完成，请立即查看设计图并确认！" ,\
                                                                  status = "未确认设计" , publication_date = datetime.datetime.now(), \
                                                                  isactived=False)
                        pmessage.save()
                    if project.operator_p_id > 0 :
                        pmessage = project_operator_bussniess_message(userid_id=project.operator_p_id , project_id = pid ,\
                                                                  user_type = "运营" ,\
                                                                  title = "设计完成，请立即查看设计图并确认！" ,\
                                                                  status = "未确认设计" , publication_date = datetime.datetime.now(), \
                                                                  isactived=False)
                        pmessage.save()
                    if project.customer_service_id > 0 :
                        pmessage = project_operator_bussniess_message(userid_id=project.customer_service_id , project_id = pid ,\
                                                                  user_type = "客服" ,\
                                                                  title = "设计完成，请立即查看设计图并确认！" ,\
                                                                  status = "未确认设计" , publication_date = datetime.datetime.now(), \
                                                                  isactived=False)
                        pmessage.save() 
                                                




            if status == u"测试中":
                flag = 0
                prolist = public_message.objects.filter\
                (project=pid).filter(isactived=3).order_by("-id")
                try:
                    prolist[0].isactived
                except IndexError:
                    try:
                        request.session['id']
                    except KeyError:
                        return HttpResponseRedirect("/nologin")
                    else:
                        flag = 1                        
                else:
                    if prolist[0].isactived != 3:
                        try:
                            request.session['id']
                        except KeyError:
                            return HttpResponseRedirect("/nologin")
                        else:
                            flag = 1
                if flag == 1:        
                    usrid = request.session['id']
                    project = models.project.objects.get(id=pid)
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                    content = project.project + u"于"+time+u"已发测试版，请在上线前联系项目负责人并确认验收！"    
                    uids = []
                    if project.business_man_id > 0 :
                        uids.append(project.business_man_id)
                    if project.operator_p_id > 0 :
                        uids.append(project.operator_p_id)
                    if project.customer_service_id > 0 :
                        uids.append(project.customer_service_id)
                    for uid in uids :
                        #存表public_message
                        pmessage = public_message(project=pid, \
                                              publisher=uid, content=content, type_p="message", \
                                              publication_date=datetime.datetime.now(), \
                                              delay_status = "未确认" ,\
                                              isactived=3)
                        pmessage.save()
                        #存表project_user_message
                        #存该项目的业务负责人、客服负责人和运营负责人，只有这三个个人哦 
                        messageid = public_message.objects.filter(publisher = uid).order_by("-id")[0]
                        ppmessage = project_user_message(userid_id = uid , messageid_id = messageid.id ,\
                                                        project_id = pid , isactived = True )
                        ppmessage.save()
                    #存表project_operator_bussniess_message
                    #存该项目的业务负责人、客服负责人和运营负责人，只有这三个个人哦
                    if project.business_man_id > 0 :
                        pmessage = project_operator_bussniess_message(userid_id=project.business_man_id , project_id = pid ,\
                                                                  user_type = "业务" ,\
                                                                  title = "已发测试版，请在上线前联系项目负责人并确认验收！" ,\
                                                                  status = "项目未验收" , publication_date = datetime.datetime.now(), \
                                                                  isactived=False)
                        pmessage.save()
                    if project.operator_p_id > 0 :
                        pmessage = project_operator_bussniess_message(userid_id=project.operator_p_id , project_id = pid ,\
                                                                  user_type = "运营" ,\
                                                                  title = "已发测试版，请在上线前联系项目负责人并确认验收！" ,\
                                                                  status = "项目未验收" , publication_date = datetime.datetime.now(), \
                                                                  isactived=False)
                        pmessage.save()
                    if project.customer_service_id > 0 :
                        pmessage = project_operator_bussniess_message(userid_id=project.customer_service_id , project_id = pid ,\
                                                                  user_type = "客服" ,\
                                                                  title = "已发测试版，请在上线前联系项目负责人并确认验收！" ,\
                                                                  status = "项目未验收" , publication_date = datetime.datetime.now(), \
                                                                  isactived=False)
                        pmessage.save()
                                                
            


            #给项目负责人添加申请延期权限
            #User.objects.get(username=musername).user_permissions.add(34)

            #上线后插条公告,如果表中项目ID存在,排序看isactived是否为0,如果不存在该项目ID或最小的isactived=0,则插入公告
            if status == u"已上线":
                flag = 0
                prolist = public_message.objects.filter\
                (project=pid).order_by("isactived")
                try:
                    prolist[0].isactived
                except IndexError:
                    try:
                        request.session['id']
                    except KeyError:
                        return HttpResponseRedirect("/nologin")
                    else:
                        flag = 1                        
                else:
                    if prolist[0].isactived != 0:
                        try:
                            request.session['id']
                        except KeyError:
                            return HttpResponseRedirect("/nologin")
                        else:
                            flag = 1
                if flag == 1:        
                    usrid = request.session['id']
                    project = models.project.objects.get(id=pid)
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
                    content = project.project + u"于"+time+u"已上线"
                    pmessage = public_message(project=pid, \
                                              publisher=usrid, content=content, type_p="notice", \
                                              publication_date=datetime.datetime.now(), \
                                              isactived=False)
                    pmessage.save()
                    
                    ###
                    #先判断在项目上线之前有没有留言的人
                    try:
                        related_user = models.project_feedback.objects.filter(project_id=pid)
                    except:
                        None
                    else:
                        #项目上线，给留言者发的消息存在消息表中
                        string = project.project + u"已上线，您可以去体验并跟踪反馈机构的体验效果啦"
                        pub_message = public_message(project=pid, publisher=usrid, content=string, \
                            type_p="message", publication_date=datetime.datetime.now(), delay_status="已上线", isactived=1)
                        pub_message.save()
                        #先判断在项目上线之前有没有留言的人
                        #从留言表中把此项目相关的留言数据读取出来（留言者id）
                        message = public_message.objects.filter(project=pid).order_by("-id")[0]
                        #给项目和消息创建关系
                        for i in related_user:
                            uid = i.feedback_member_id
                            megid = message.id
                            pro_u_message = project_user_message(userid_id=uid, messageid_id=megid, project_id=pid, isactived='1')
                            pro_u_message.save()   
                    ### 
                    
                    project.real_launch_date = datetime.datetime.now()
                    project.save()                   
            return redirect('/projectlist/')
        else:
            dateloop = ['psdate', 'pedate', 'dsdate', 'dedate', 'tsdate', 'tedate', 'startdate', 'plandate']
            prodate = []
            for item in dateloop:
                cdate = request.POST[item]
                if cdate:
                    idate = datetime.datetime.strptime(cdate, "%Y-%m-%d")
                else:
                    idate = None
                prodate.append(idate)
            if request.POST['leader']:
                luser = models.user.objects.get(id=request.POST['leader'])
            else:
                luser = None
            relateduser0 = request.POST['relateduser0']
            relateduser1 = request.POST['relateduser1']
            relateduser2 = request.POST['relateduser2']
            relateduser3 = request.POST['relateduser3']
            relateduser4 = request.POST['relateduser4']
            relateduser5 = request.POST['relateduser5']
            
            relateduser = [relateduser0, relateduser1, relateduser2, relateduser3, relateduser4, relateduser5]
            people = []
            allpeople = []
            for i in range(len(relateduser)):
                relateduser[i] = relateduser[i].replace(" ", "").split(",")
            # pd = []
            # dev = []
            # qa = []           
                for uid in relateduser[i]:
                    if uid:
                        tuser = models.user.objects.get(id=int(uid))
                        people.append(tuser)
                allpeople.append(people)
                        # if tuser.department_id == 1:
                        #     qa.append(tuser)
                        # elif tuser.department_id == 3:
                        #     pd.append(tuser)
                        # else:
                        #     dev.append(tuser)
            related_user = {'pd':allpeople[0], 'dev': allpeople[1], 'dev': allpeople[2], \
            'bm': allpeople[3], 'cs': allpeople[4], 'op': allpeople[5]}
            dpid = request.POST['designer']
            tpid = request.POST['tester']
            if dpid:
                dpid = int(dpid)
            if tpid:
                tpid = int(tpid)

            pro = {'priority':request.POST['priority'],
                   'project':request.POST['pname'],
                   'status_p':request.POST['status'],
                   'leader_p_id':request.POST['leader'],
                   'designer_p_id':dpid,
                   'tester_p_id':tpid,
                   'start_date':prodate[6],
                   'expect_launch_date':prodate[7],
                   'estimated_product_start_date':prodate[0],
                   'estimated_product_end_date':prodate[1],
                   'estimated_develop_start_date':prodate[2],
                   'estimated_develop_end_date':prodate[3],
                   'estimated_test_start_date':prodate[4],
                   'estimated_test_end_date':prodate[5],
                   'blueprint_p':request.POST['ppath'],
                   'develop_plan_p':request.POST['dppath'],
                   'test_plan_p':request.POST['tppath'],
                   'test_case_p':request.POST['tcpath'],
                   'test_report_p':request.POST['trpath'],}

            dt_temp = {}
            dt = {}
            #处理时间为空,无法计算时间差
            if (pro['estimated_product_end_date'] != None) & (pro['estimated_product_start_date'] != None):
                dt_temp['p'] = pro['estimated_product_end_date'] - pro['estimated_product_start_date']
                dt['ptime'] = int(dt_temp['p'].days+1)
            else:
                dt['ptime'] = 0
            if (pro['estimated_develop_end_date'] != None) & (pro['estimated_develop_start_date'] != None):
                dt_temp['d'] = pro['estimated_develop_end_date'] - pro['estimated_develop_start_date']
                dt['dtime'] = int(dt_temp['d'].days+1)
            else:
               dt['dtime'] = 0
            if (pro['estimated_test_end_date'] != None) & (pro['estimated_test_start_date'] != None):
                dt_temp['t'] = pro['estimated_test_end_date'] - pro['estimated_test_start_date']
                dt['ttime'] = int(dt_temp['t'].days+1)
            else:
                dt['ttime'] = 0

            res = {'pro':pro, 'user':luser, 'reuser':related_user, 'dt': dt}
            return render_to_response('newproject.html', \
                {'res':res, 'form':form,'editdate':editdate}, context_instance=RequestContext(request))

    return render_to_response('newproject.html', \
        {'form':form, 'editdate':editdate}, context_instance=RequestContext(request))
    
def project_list(request):
    #没登陆的提示去登录
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/nologin")
    #判断是否登录，给一个是否登录的标记值,logintag=1为已登录
    #以下是权限标记，createtag是发布相似的权限
    createtag = 0
    logintag = 0
    changetag = 0
    delaytag = 0
    deletetag = 0
    edittag = 0
    user_id = 0
    #PM的pM的tag
    auth_changetag = 0
    #判断是否登录
    if  request.user.is_authenticated():
        logintag = 1
        #user_id = request.session['id']
    if logintag == 1:

        if request.user.has_perm("project.change_public_message"):
            changetag = 1
        if request.user.has_perm('project.change_project'):
            edittag = 1
        if request.user.has_perm("project.add_project_delay"):
            delaytag = 1
        if request.user.has_perm("project.delete_project"):
            deletetag = 1
        if request.user.has_perm("auth.change_permission"):
            auth_changetag = 1
        if  request.user.has_perm('project.add_project'):
            createtag = 1

    #notice
    noticess = public_message.objects.filter(type_p='notice').order_by('-id')
    count = len(noticess)
    notices = noticess[:5]   	
    ##
    projectlist = None
    puser = None
    project_id = ""if isNone(request.GET.get("id"))else request.GET.get("id")
    project_name = ""if isNone(request.GET.get("project"))else request.GET.get("project")

    start_date_s = "" if isNone(request.GET.get("start_date_s")) else request.GET.get("start_date_s")

    end_date_s = "" if isNone(request.GET.get("end_date_s")) else request.GET.get("end_date_s")
    status_p = "" if isNone(request.GET.get("status_p")) else request.GET.get("status_p")
    leader_p = "" if isNone(request.GET.get("leader_p")) else request.GET.get("leader_p")
    type_p = "" if isNone(request.GET.get("type_p")) else request.GET.get("type_p")

    #将get到的日期参数由string类型（实际type的时候显示是unicode，暂时未知）转换成datetime类型。
    #strptime是将str类型转换为struct_time,然后再用datetime.date将time类型转换为datetime类型
    #"*"表示将列表中的数据作为函数的参数，如果是**则是将字典中的数据作为函数的参数
    if not isNone(start_date_s):
        start_time = time.strptime(start_date_s ,"%Y-%m-%d")
        start_date_s = datetime.date(*start_time[:3])
    if not isNone(end_date_s):
        end_time = time.strptime(end_date_s ,"%Y-%m-%d")
        end_date_s = datetime.date(*end_time[:3])



    project_user_list = None
    puser = project_user.objects.all()
    #projectlist = project.objects.all()
    if request.method == 'POST':
        search_form = ProjectSearchForm(request.POST)
        if search_form.is_valid():
            project_id = search_form.cleaned_data['id']
            project_name = search_form.cleaned_data['project']
            start_date_s = search_form.cleaned_data['start_date_s']
            print(start_date_s)
            end_date_s = search_form.cleaned_data['end_date_s']
            status_p = search_form.cleaned_data['status_p']
            leader_p = search_form.cleaned_data['leader_p']
            type_p = search_form.cleaned_data['type_p']

            projectlist = models.project.objects.filter().order_by("-status_p","-priority")
            


    else:
        projectlist = models.project.objects.all().order_by("-status_p","-priority")
    if not isNone(project_id):
        project_id=project_id.strip()
        if(project_id.isdigit()):
            projectlist = projectlist.filter(id=project_id)
        else:
            projectlist = projectlist.filter(id=0)
    if not isNone(project_name):
        projectlist = projectlist.filter(project__contains=project_name.strip())
    if not isNone(start_date_s):
        projectlist = projectlist.filter(start_date__gte=start_date_s)
    if not isNone(end_date_s):
        projectlist = projectlist.filter(start_date__lte=end_date_s)
    if not isNone(status_p):
        projectlist = projectlist.filter(status_p=status_p.strip())
    #新增的筛选项，类型
    if not isNone(type_p):
        projectlist = projectlist.filter(type_p=type_p.strip())
    if not isNone(leader_p):
        #projectlist = projectlist.filter(leader_p__username__contains=leader_p.strip())
        project_user_list = models.project_user.objects.filter(username__realname__contains=leader_p.strip())
        projectids = []
        for p in project_user_list:
            projectids.append(p.project.id)
        projectlist = projectlist.filter(pk__in=projectids)

    paginator = Paginator(projectlist, 25)
    page = request.GET.get('page')
    try:
        projectobj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projectobj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projectobj = paginator.page(paginator.num_pages)
    # 项目使用量统计    
    pcount = models.project_statistics.objects.all()
    for c in pcount:
        sql = c.sql
        db = c.db
        try:
            cursor = connections[db].cursor()
            cursor.execute(sql)
            total = cursor.fetchall()
            total_list = ''       
            for a in total:         #适合显示1列数据，若要多显示，则需要对a继续循环
                    if len(total) == 1:         #此处if, else为了调整样式好看
                        total_list = str(a[0])
                    else:
                        total_list = total_list + str(a[0]) + '\r'
                  
            c.total = total_list
            c.save()
            cursor.close()
        except:
            pass
                
    p1 = models.project_statistics.objects.distinct().values('project_id')
    filter_project =[] #每个项目只返回一组统计值最大的记录,方便页面显示
    for x in p1:
        filter_project.append(pcount.filter(project_id=x['project_id']).order_by("total")[0])
    
    return render_to_response('projectlist.html', RequestContext(request, {'projectobj':projectobj, \
            'puser':puser, 'pcount':pcount, 'fproject':filter_project,  'project_id':project_id, \
            'project_name':project_name, 'start_date_s':start_date_s, 'end_date_s':end_date_s, \
            "status_p":status_p, "leader_p":leader_p,"type_p":type_p, 'notices':notices, \
            'count':count, "logintag":logintag, "changetag":changetag, "delaytag":delaytag, "deletetag":deletetag,\
            "edittag":edittag, "user_id":user_id, "auth_changetag":auth_changetag, "createtag":createtag}))
    
def praise(request ,pid):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    p = models.project.objects.get(id=int(pid))
    praisecount = p.praise_p+1
    p.praise_p = praisecount
    p.save()


    return HttpResponse(praisecount)

def isNone(s):
    if s is None or (isinstance(s, basestring) and len(s.strip()) == 0):
        return True
    else:
        return False
    
def detail(request, pid='', nid=''):
    """
    pid是项目id
    nid为1时,表示发布与项目pid相似的项目
    """
    pro = models.project.objects.get(id=int(pid))
    user = models.user.objects.get(id=pro.leader_p_id)
    devs = models.user.objects.filter(Q(project_user__project_id=pid), Q(project_user__roles=1), Q(department_id=2) | Q(department_id=4) | Q(department_id=5) | Q(department_id=13))
    bms = models.user.objects.filter(Q(project_user__project_id=pid), Q(project_user__roles=3), Q(department_id=12) | Q(department_id=9) | Q(department_id=7))
    ops = models.user.objects.filter(Q(project_user__project_id=pid), Q(project_user__roles=4),Q(department_id=3) | Q(department_id=8) | Q(department_id=12)| Q(department_id=9) | Q(department_id=7))
    #这个列表用来存测试产品销售客服
    p_role = []
    #这个列表用来存测试产品销售客服的部门id和roles值
    dep_id = [[1,2], [3,0], [7,5]]
    for item_id in dep_id:
        p_role.append(models.user.objects.filter(project_user__project_id=pid, department_id=item_id[0], project_user__roles=item_id[1]))

    related_user = {'qa':p_role[0], 'dev': devs, 'pd': p_role[1], 'bm': bms, 'cs': p_role[2], 'op': ops}

    dt_temp = {}
    dt = {}
    #处理时间为空,无法计算时间差
    if (pro.estimated_product_end_date != None) & (pro.estimated_product_start_date != None):
        dt_temp['p'] = pro.estimated_product_end_date - pro.estimated_product_start_date
        dt['ptime'] = int(dt_temp['p'].days+1)
    else:
        dt['ptime'] = 0
    if (pro.estimated_develop_end_date != None) & (pro.estimated_develop_start_date != None):
        dt_temp['d'] = pro.estimated_develop_end_date - pro.estimated_develop_start_date
        dt['dtime'] = int(dt_temp['d'].days+1)
    else:
        dt['dtime'] = 0
    if (pro.estimated_test_end_date != None) & (pro.estimated_test_start_date != None):
        dt_temp['t'] = pro.estimated_test_end_date - pro.estimated_test_start_date
        dt['ttime'] = int(dt_temp['t'].days+1)
    else:
        dt['ttime'] = 0
    editboolean = False
    pro_sql = models.project_statistics.objects.filter(project_id=pid)
    sql = ''
    for p in pro_sql:
        sql = sql + p.item + ':' + p.db + ':' + p.sql + ';' 
    if sql=='':
        status = '未填写'
    else:
        status = '已填写'
#各部门负责人确认状态  
    confirmation = {}
    bm_status = models.project_operator_bussniess_message.objects.filter(project_id=pid, user_type='bm').order_by("id")
    a = 0
    if bm_status:
        bm_check = None
        for item in bm_status:            
            if item.confirm_design_date:
                bm_design_date = item.confirm_design_date
                bm_design = bm_design_date.strftime("%Y-%m-%d %H:%I") + item.status
            else:
                if item.check_date:
                    bm_check_date = item.check_date
                    bm_check = bm_check_date.strftime("%Y-%m-%d %H:%I") + item.status
                else:
                    print item.confirm_design_date
                    if a == 0:
                        bm_design = item.status
                    else:
                        bm_check = item.status
            a = a + 1
        confirmation['bm_design'] = bm_design
        if bm_check:
            confirmation['bm_check'] = bm_check
    op_status = models.project_operator_bussniess_message.objects.filter(project_id=pid, user_type='op')
    a = 0
    if op_status:
        op_check = None
        for item in op_status:            
            if item.confirm_design_date:
                    op_design_date = item.confirm_design_date
                    op_design = op_design_date.strftime("%Y-%m-%d %H:%I") + item.status
            else:
                if item.check_date:
                    op_check_date = item.check_date
                    op_check = op_check_date.strftime("%Y-%m-%d %H:%I") + item.status
                else:
                    if a == 0:
                        op_design = item.status
                    else:
                        op_check = item.status
            a = a + 1
        confirmation['op_design'] = op_design
        if op_check:
            confirmation['op_check'] = op_check
    cs_status = models.project_operator_bussniess_message.objects.filter(project_id=pid, user_type='cs')
    a = 0
    if cs_status:
        cs_check = None
        for item in cs_status:            
            if item.confirm_design_date:
                cs_design_date = item.confirm_design_date
                cs_design = cs_design_date.strftime("%Y-%m-%d %H:%I") + item.status
            else:
                if item.check_date:
                    cs_check_date = item.check_date
                    cs_check = cs_check_date.strftime("%Y-%m-%d %H:%I") + item.status
                else:
                    if a == 0:
                        cs_design = item.status
                    else:
                        cs_check = item.status
            a = a + 1
        confirmation['cs_design'] = cs_design
        if cs_check:
            confirmation['cs_check'] = cs_check
    
    try:
        request.user             
        if (request.user.has_perm('auth.change_permission') or request.session['id']==pro.leader_p_id \
            or request.session['id']==pro.designer_p_id or request.session['id']==pro.tester_p_id):
            editboolean = True
    finally:
        if '/detail/' in request.path:
            res = {'pro':pro, 'user':user, 'dt': dt, 'reuser': related_user, 'editbool': editboolean, 
                   'sql': status, 'confirmation': confirmation}
            return render_to_response('detail.html', {'res': res})
        elif '/editproject' in request.path:
            
            edittag = 1
            editdate = 1
            isdevs = 1
            isope = 0
            if nid == '1':
                #此时是在发布相似项目
                edittag = 0
            else:
                #在编辑项目
                user_id = request.session['id']
                dep_id = models.user.objects.filter(id=user_id)[0].department_id

                #isdevs标记当前登陆者是不是技术人员      
                if dep_id not in [1,2,3,4,5,13]:
                    isdevs = 0
                    bs_id = models.project.objects.get(id=pid).operator_p_id
                    if user_id == bs_id:
                        isope = 1

                if not request.user.has_perm('auth.change_permission'):
                    editdate = 0

            res = {'pro':pro, 'user':user, 'dt': dt, 'reuser': related_user, 'request': edittag, 'editid':nid, 'sql': sql}
            return render_to_response('newproject.html', {'res': res, 'editdate':editdate, 'isdevs':isdevs, 'isope':isope})

def show_person(request):
    roles = request.GET['role']
    key = 0
    if roles == "tes":
        key = 1
    elif roles == "dev":
        key = 2
    elif roles == "pro":
        key = 3
    elif roles =="sal":
        key = 12
    elif roles =="ope":
        key = 8
    elif roles == "com":
        key = 7
    else:
        key = 0

    if key == 2:
        person = models.user.objects.filter(Q(department_id=key) | Q(department_id=4) | Q(department_id=5) | Q(department_id=13), Q(isactived=1))
    elif key == 12:
        person = models.user.objects.filter(Q(department_id=key) | Q(department_id=9) | Q(department_id=7), Q(isactived=1))
    elif key == 8:
        person = models.user.objects.filter(Q(department_id=key) | Q(department_id=3) | Q(department_id=12)| \
            Q(department_id=9) | Q(department_id=7), Q(isactived=1))
    else:
        person = models.user.objects.filter(department_id=key, isactived=1)
    person_rs = []
    num = len(person)
    if num == 0:
        rrs = {"person":person_rs}
        person_rs = json.dumps(rrs)
        return HttpResponse(person_rs)
    for item in person:
        uid = item.id
        realname = item.realname
        dic = {'id':int(uid), 'realname':realname}
        person_rs.append(dic)

    rrs = {"person":person_rs}
    person_rs = json.dumps(rrs)
    return HttpResponse(person_rs)

def psearch(request):
    key = request.GET['key']
    role = request.GET['role']
    ptype = 0
    if role == "tes":
        ptype = 1
    elif role == "dev":
        ptype = 2
    elif role == "pro":
        ptype = 3
    elif role =="sal":
        ptype = 12
    elif role =="ope":
        ptype = 8
    elif role == "com":
        ptype = 7
    else:
        ptype = 0
    
    if len(key) == 0:
        if ptype == 2:
            prs = models.user.objects.filter(Q(isactived=1),Q(department_id=ptype)|Q(department_id=4)|Q(department_id=5)|Q(department_id=13))
        elif ptype == 12:
            person = models.user.objects.filter(Q(department_id=ptype) | Q(department_id=9) | Q(department_id=7), Q(isactived=1))
        elif ptype == 8:
            person = models.user.objects.filter(Q(department_id=ptype) | Q(department_id=3) | Q(department_id=12)| \
                Q(department_id=9) | Q(department_id=7), Q(isactived=1))
        else:
            prs = models.user.objects.filter(department_id=ptype, isactived=1)
    else:
        if ptype == 2:
            prs = models.user.objects.filter(Q(realname__contains=key), Q(isactived=1), Q(department_id=ptype)|Q(department_id=4)|Q(department_id=5)|Q(department_id=13))
        elif ptype == 12:
            person = models.user.objects.filter(Q(realname__contains=key),Q(department_id=ptype) | Q(department_id=9) | Q(department_id=7), Q(isactived=1))
        elif ptype == 8:
            person = models.user.objects.filter(Q(realname__contains=key),Q(department_id=ptype) | Q(department_id=3) | Q(department_id=12)| \
                Q(department_id=9) | Q(department_id=7), Q(isactived=1))
        else:
            prs = models.user.objects.filter(realname__contains=key, department_id=ptype, isactived=1)
            
    search_rs = []
    if len(prs) > 0:
        for item in prs:
            dic = {'id':item.id, 'realname':item.realname}
            search_rs.append(dic)
        rrs = {"person":search_rs}
        search_rs = json.dumps(rrs)
    else:
        rrs = {"person":search_rs}
        search_rs = json.dumps(rrs)
    return HttpResponse(search_rs)

#通用头
def user_info(request):
    result={}
    try:
        if request.session['username']:
            projectlist = models.project.objects.filter()
            project_user_list = models.project_user.objects.filter(username__username = request.session['username'])
            projectids = []
            for p in project_user_list:
                projectids.append(p.project.id) 
            projectlist = projectlist.filter(pk__in = projectids)       
            res = projectlist.exclude(Q(status_p = u'已上线') | Q(status_p = u'暂停')).order_by("-id")
            pro_num=res.count()
            result['pro_num']=pro_num
   
            userid = request.session['id']
            messsage = project_user_message.objects.filter(userid_id = userid)
            message_num = messsage.count()
            result['message_num'] = message_num
                       
            username = request.session['username']
            realname = request.session['realname']
            result['username'] = username
            result['realname'] = realname      
    except KeyError:
            result['pro_num'] = 0
            result['message_num'] = 0
            result['username'] = 'GUEST'
            result['realname'] = 'GUEST' 
    rs = json.dumps(result)
    return HttpResponse(rs)
#homepage
def personal_homepage(request):
    try:
        request.session['username']
        projectlist = models.project.objects.filter()
        #print projectlist
        project_user_list = models.project_user.objects.filter(username__username = request.session['username'])
    except KeyError:
        return HttpResponseRedirect("/nologin")
    #设计变更
    changetag = 0
    if request.user.has_perm('project.change_public_message'):
        changetag = 1
    #编辑
    edittag = 0
    if request.user.has_perm('project.change_project'):
        edittag = 1
    #延期申请权限
    userid1 = 0
    if request.user.is_authenticated():
        userid1 = request.session['id']
    delaytag = 0
    if request.user.has_perm('project.add_project_delay'):
        delaytag = 1
    #暂停
    pausetag = 0 
    if request.user.has_perm('project.delete_project'):
        pausetag = 1  
    #删除
    deletetag = 0
    if request.user.has_perm('project.delete_project'):
        deletetag = 1 
    pm=0
    if request.user.has_perm("auth.change_permission"):
            pm = 1
    projectids = []
    for p in project_user_list:
        projectids.append(p.project.id)
    projectlist = projectlist.filter(pk__in = projectids)
    result = projectlist.exclude(Q(status_p = u'已上线') | Q(status_p = u'暂停')).order_by("-id")   
    result1 = projectlist.exclude(~Q(status_p = u'已上线')& ~Q(status_p = u'暂停')).order_by("-id")
    puser = models.project_user.objects.all()
    """分页"""
    paginator = Paginator(result1, 25)
    page = request.GET.get('page')
    try:
        projectobj = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projectobj = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projectobj = paginator.page(paginator.num_pages)
    #message
    userid = request.session['id']
    dealdelay = 0
    countdelay = 0
    if request.user.has_perm('project.change_project_delay'):
        dealdelay = 1
        delays = project_delay.objects.filter(result__isnull=True,).order_by('apply_date')
        countdelay = delays.count()
    i = 0
    tests= project_user_message.objects.filter(userid_id = userid)
    lists = []
    messagess = []
    for test in tests:
        lists.append(test.messageid_id)
    messagess = public_message.objects.filter(pk__in = lists).filter(type_p = "message").order_by('-id')  
    count = messagess.count()
    messages = messagess[:4]   
    return render_to_response('personal_homepage.html', \
        {'projectobj':projectobj, 'result':result, 'result1':result1, 'puser':puser, 'messages': messages, \
         'count':count, 'dealdelay':dealdelay, 'changetag':changetag, 'edittag':edittag, 'delaytag':delaytag, 'pausetag':pausetag, 'deletetag':deletetag, 'pm':pm, 'userid1':userid1,'countdelay':countdelay})
def deleteproject(request,id,url):
    delpro=get_object_or_404(project,pk=int(id))    
    delpro.delete()
    return HttpResponseRedirect(url)
def pauseproject(request, id, url):
    pausepro = get_object_or_404(project, pk = int(id))
    pausepro.status_p ='暂停'
    pausepro.save()
    return HttpResponseRedirect(url)
def delayproject(request, url):
    if request.method == 'POST':
        form = delayprojectForm(request.POST)
        if form.is_valid():
            delayid = form.cleaned_data['delayid']
            delay_date = form.cleaned_data['delay_date']
            delay_reason = form.cleaned_data['delay_reason']
            delpro = models.project.objects.get(id=delayid)
            uid = delpro.leader_p
            protitle = delpro.project
            delay_p = project_delay(application = uid, project_id = delayid, delay_to_date = delay_date, \
                apply_date = datetime.datetime.now(), title = protitle, reason = delay_reason, isactived = 1)
            delay_p.save()                   
    return HttpResponseRedirect(url)
def changedesign(request, url):          
    if request.method == 'POST':
        form = changedesignForm(request.POST)
        if form.is_valid():
            changeid = form.cleaned_data['changeid']
            cont = form.cleaned_data['cont'].replace('\r\n','<br/> ')
            dpath = form.cleaned_data['dpath'].replace('\r\n','<br/> ')
            chd = models.project.objects.get(id = changeid)
            uid = request.session['id']
            #chd.blueprint_p=dpath
            #chd.save()
            string = chd.project+u' : ' + '<br/> ' +cont + '<br/> ' + dpath
            pub_message = public_message(project = changeid, publisher = uid, content = string, type_p = "message",\
             publication_date = datetime.datetime.now(), isactived = "1")
            pub_message.save()
            related_user = models.user.objects.filter(project_user__project_id = changeid)
            message = public_message.objects.filter(project=changeid).order_by("-id")[0]            
            for i in related_user:
                uid = i.id
                megid = message.id
                pro_u_message = project_user_message(userid_id = uid, messageid_id = megid, \
                    project_id = changeid, isactived = '1')
                pro_u_message.save()           
    return HttpResponseRedirect(url)
    #return render_to_response('personal_homepage.html', {'form': form})

#资源管理
def judge(request):
    try:
        if request.session['username']:
            username = request.session['username']
        Position_level = models.user.objects.get(username=\
        username).Position_level
        if Position_level == '1' or request.user.has_perm('project.change_user'):
            return redirect('/show_user/')
        else:
            return redirect('/show_source/')
    except KeyError:
        return redirect('/nologin/')
def show_source(request):
    try:
        if request.session['username']:
            username = request.session['username']
            department_id = models.user.objects.get(username=\
            username).department_id
        department_id = department_id
        department = models.department.objects.get(id=\
        department_id).department
        department_list = models.department.objects.all()
        level_1_list = models.user.objects.filter(department_id=\
        department_id, Position_level="1")
        level_2_list = models.user.objects.filter(department_id=\
        department_id, Position_level="2")
        level_3_list = models.user.objects.filter(department_id=\
        department_id, Position_level="3")
        return render_to_response('show_source.html', locals())
    except KeyError:
        return redirect('/nologin/')

@csrf_exempt
def show_user2(request):
    department = request.POST['department']
    if department == '请选择':
        department_id = 0
    else:
        depart = models.department.objects.all()
        departdic = {}
        for item in depart:
            departdic[item.department] = item.id
        department_id = departdic[department]
    level_1_list = models.user.objects.filter(department_id=\
    department_id, Position_level="1")
    level_2_list = models.user.objects.filter(department_id=\
    department_id, Position_level="2")
    level_3_list = models.user.objects.filter(department_id=\
    department_id, Position_level="3")
    department_list = models.department.objects.all()
    return render_to_response('show_source.html', locals())

@csrf_exempt
def show_user(request):
    try:
        if request.session['username']:
            username = request.session['username']
            department_id = models.user.objects.get(username=\
            username).department_id
        department_id = department_id
        department = models.department.objects.get(id=\
        department_id).department
        if request.method == 'POST':
            department = request.POST['department']
            if department == '请选择':
                department_id = 0
            else:
                depart = models.department.objects.all()
                departdic = {}
                for item in depart:
                    departdic[item.department] = item.id
                department_id = departdic[department]
        else:
            department_id = department_id
        level_list = models.user.objects.filter(department_id=\
        department_id)
        level_1_list = models.user.objects.filter(department_id=\
        department_id, Position_level="1")
        level_2_list = models.user.objects.filter(department_id=\
        department_id, Position_level="2")
        level_3_list = models.user.objects.filter(department_id=\
        department_id, Position_level="3")
        department_list = models.department.objects.all()
        return render_to_response('sourcemanage.html', locals())
    except KeyError:
        return redirect('/nologin/')

@csrf_exempt
def Insert_user(request, id, id2, id3):
    if request.session['username']:
        username = request.session['username']
        department_id = models.user.objects.get(username=\
        username).department_id
    department_id = department_id
    department = request.POST['department']
    if department == '请选择':
        department_id = 0
    else:
        depart = models.department.objects.all()
        departdic = {}
        for item in depart:
            departdic[item.department] = item.id
        department_id = departdic[department]
    if id == '1':
        id = request.POST['level_1']
        user = models.user.objects.filter(department_id=\
        department_id, id=id).update(Position_level='1')
    elif id == '2':
        id = request.POST['level_2a']
        user = models.user.objects.filter(department_id=department_id, \
        id=id).update(Position_level='2')
    elif id == '3':
        id = request.POST['level_3a']
        user = models.user.objects.filter(department_id=department_id, \
        id=id).update(Position_level='3')
    elif id == '4':
        id = request.POST['level_1']
        user = models.user.objects.filter(department_id=department_id, \
        id=id).update(Position_level='0')
    elif id == '5':
        user = models.user.objects.filter(department_id=department_id, \
        id=id2).update(Position_level='0')
    elif id == '6':
        user = models.user.objects.filter(department_id=department_id, \
        id=id2).update(Position_level='0')
    elif id == '7':
        id = request.POST['level_1']
        user = models.user.objects.get(department_id=department_id, \
        id=id)
        user.delete()
    elif id == '8':
        user = models.user.objects.get(department_id=department_id, \
        id=id2)
        user.delete()
    elif id == '9':
        user = models.user.objects.get(department_id=department_id, \
        id=id2)
        user.delete()
    elif id == '10':
        user = models.user.objects.filter(department_id=department_id, \
        id=id3).update(Position_level='0')
        user = models.user.objects.filter(department_id=department_id, \
        id=id2).update(Position_level='2')
    elif id == '11':
        user = models.user.objects.filter(department_id=department_id, \
        id=id3).update(Position_level='0')
        user = models.user.objects.filter(department_id=department_id, \
        id=id2).update(Position_level='3')
    elif id == '12':
        user = models.user.objects.filter(department_id=department_id, \
        id=id3).update(Position_level='0')
        user = models.user.objects.filter(department_id=department_id, \
        id=id2).update(Position_level='1')
    return redirect('/show_user/')
#延期
def delay(request):

    if not request.session['id']:
        return HttpResponseRedirect("/nologin")

    if not request.user.has_perm('project.change_project_delay'):
        return HttpResponseRedirect("/noperm")

    delays = project_delay.objects.filter(isactived__isnull= False).order_by('-id')
    global  projectobj
    paginator = Paginator(delays, 25)
    page = request.GET.get('page')
    try:
        projectobj = paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer, deliver first page.
        projectobj = paginator.page(1)
    except EmptyPage:
        #If page is out of range (e.g. 9999), deliver last page of results.
        projectobj = paginator.page(paginator.num_pages)
    return render_to_response('delay.html', RequestContext(request, {'projectobj': projectobj}))

#公告
def notice(request):
    global search_key
    search_key=''
    if request.method == 'POST':  # 如果是post请求
        wds = request.POST
        try:
            noticetext = wds['wd']
            search_key=noticetext
            notices = public_message.objects.filter(content__icontains=noticetext).filter(type_p="notice").order_by("-id")

        except Exception:
            notices = public_message.objects.filter(type_p="notice").order_by("-id")
    else:  # Get请求
        wds = request.GET
        try:
            search_key = wds['search_key']
            notices = public_message.objects.filter(type_p="notice").filter(content__icontains=search_key).order_by("-id")
        except Exception:
            notices = public_message.objects.filter(type_p="notice").order_by("-id")
    global  projectobj
    paginator = Paginator(notices, 25)
    page = request.GET.get('page')
    try:
        projectobj = paginator.page(page)
    except PageNotAnInteger:
    #If page is not an integer, deliver first page.
        projectobj = paginator.page(1)
    except EmptyPage:
    #If page is out of range (e.g. 9999), deliver last page of results.
        projectobj = paginator.page(paginator.num_pages)
    return render_to_response('notice.html', RequestContext(request, {'projectobj': projectobj,'search_key':search_key}))

@csrf_exempt

#历史消息
def historymessage(request):
    global search_key
    search_key=''
    # 查询与用户相关的消息
    if request.session['id']:
        useid = request.session['id']
    tests = project_user_message.objects.filter(userid_id=useid)
    lists = []
    for test in tests:
        lists.append(test.messageid_id)
    if request.method == 'POST':  # 如果是post请求
        wds = request.POST
        try:
            messagetext = wds['wd']
            search_key= messagetext
            messages = public_message.objects.filter(pk__in=lists).filter(content__icontains=messagetext).filter(type_p="message").order_by('-id')
        except Exception:
            messages = public_message.objects.filter(pk__in=lists).filter(type_p="message").order_by('-id')
    else:  # Get请求
        wds = request.GET
        try:
            search_key = wds['search_key']
            messages = public_message.objects.filter(pk__in=lists).filter(type_p="message").filter(content__icontains=search_key).order_by('-id')
        except Exception:
            messages = public_message.objects.filter(pk__in=lists).filter(type_p="message").order_by('-id')
    global  projectobj
    paginator = Paginator(messages, 25)
    page = request.GET.get('page')
    try:
        projectobj = paginator.page(page)
    except PageNotAnInteger:
    #If page is not an integer, deliver first page.
        projectobj = paginator.page(1)
    except EmptyPage:
        projectobj = paginator.page(paginator.num_pages)
    return render_to_response('historymessage.html', RequestContext(request, {'projectobj': projectobj,'search_key':search_key}))

#拒绝
def refuse(request):
    if request.method == 'POST':

        form = TestForm(request.POST)
        if form.is_valid():
            delayid = form.cleaned_data['delayid']
            reason = form.cleaned_data['reason']
            refusedelay = project_delay.objects.get(id=delayid)
            project_id = refusedelay.project_id
            deltitle = refusedelay.title
            string = deltitle+u"申请延期被拒绝，理由"+reason
            #delpro=models.project.objects.get(id=delayid)
            if request.session['id']:

                useid = request.session['id']
                pub_message = public_message(project=project_id, publisher=useid, content=string, \
                    type_p="message", publication_date=datetime.datetime.now(), delay_status="已拒绝", isactived="1")
            #refusedelay.reason = reason
                refusedelay.result = "已拒绝"
                refusedelay.isactived = 0
                refusedelay.save()
                pub_message.save()
                related_user = models.user.objects.filter(project_user__project_id=project_id)
                message = public_message.objects.filter(project=project_id).order_by("-id")[0]
            for i in related_user:
                uid = i.id
                megid = message.id
                pro_u_message = project_user_message(userid_id=uid, messageid_id=megid, project_id=project_id, isactived='1')
                pro_u_message.save()
    return HttpResponseRedirect('/delay/')

#接受
def approve(request):
    if request.method == 'POST':
        form = Approveform(request.POST)
        if form.is_valid():
            delayid1 = form.cleaned_data['delayid1']
            approvedelay = project_delay.objects.get(id=delayid1)
            project_id = approvedelay.project_id
            deltitle = approvedelay.title
            delaydate= approvedelay.delay_to_date
            del_to_date = str(delaydate)
            string = deltitle + u"延期至：" + del_to_date
            pro = project.objects.get(id=project_id)
            pro.expect_launch_date = delaydate
            pro.save()
            #delpro=project_delay.objects.get(id=delayid1)
        if request.session['id']:
            useid = request.session['id']
            pub_message = public_message(project=project_id, publisher=useid, content=string, type_p="notice", \
                publication_date=datetime.datetime.now(), delay_status="已批准", isactived="1")
            #approvedelay.reason = reason

            approvedelay.isactived = 0
            approvedelay.result = "已批准"
            approvedelay.save()
            pub_message.save()
    return HttpResponseRedirect('/delay/')


#负责人确认消息
def confirmmessage(request):
    if request.session['id']:
        useid = request.session['id']
    if request.method == 'POST':
        form = ConmessageForm(request.POST)
        if form.is_valid(): 
            #public_message修改状态已确认
            messageid = form.cleaned_data['conmessageid']
            conmessage = public_message.objects.get(publisher=useid, id=messageid)
            conmessage.delay_status = "已确认"
            reconmessage = conmessage
            conmessage.save()
            #project_operator_bussniess_message修改状态、插入确认时间
            #如果public_message的isactived为2，就是设计需要确认
            #如果public_message的isactived为3，就是已发测试版本需要确认
            if  reconmessage.isactived==3:
                pmessage = project_operator_bussniess_message.objects.get(userid_id=useid , project_id = conmessage.project ,\
                                                                  status = "项目未验收" )
                pmessage.check_date = datetime.datetime.now()
                pmessage.status = "项目已验收"
            if reconmessage.isactived==2:
                pmessage = project_operator_bussniess_message.objects.get(userid_id=useid , project_id = conmessage.project ,\
                                                                  status = "未确认设计" )
                pmessage.confirm_design_date = datetime.datetime.now()
                pmessage.status = "已确认设计"
            pmessage.save()
    return HttpResponseRedirect('/historymessage/')


#删除历史消息
def deletehistory(request):
    if request.session['id']:
        useid = request.session['id']
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            messageid = form.cleaned_data['messageid']
            usermessage = project_user_message.objects.get(userid_id=useid, messageid_id=messageid)
            usermessage.delete()
    tests = project_user_message.objects.filter(userid_id=useid)
    lists = []
    for test in tests:
        lists.append(test.messageid_id)
    return HttpResponseRedirect('/historymessage/')

#删除公告
def deletenotice(request):
    if request.session['id']:
        useid = request.session['id']
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            noticeid = form.cleaned_data['noticeid']
            usernotice = project_user_message.objects.get(userid_id=useid, messageid_id=noticeid)
            usernotice.delete()
    tests = project_user_message.objects.filter(userid_id=useid)
    lists = []
    for test in tests:
        lists.append(test.messageid_id)
    return HttpResponseRedirect('/notice/')

#清空历史消息
def emptyehistory(request):
    if request.session['id']:
        useid = request.session['id']
    tests = project_user_message.objects.filter(userid_id=useid)
    lists = []
    if request.method == 'POST':
        for test in tests:
            test.delete()
    return HttpResponseRedirect('/historymessage/')    
def initdata(request):
    #auth_group
    group1 = Group(id=1,name='项目经理权限--新建、编辑、删除、暂停、延期处理、发布相似')
    group1.save()
    group2 = Group(id=2,name='资源管理权限--编辑部门人员')
    group2.save()
    group3 = Group(id=3,name='产品部门权限--设计变更')
    group3.save()
    group4 = Group(id=4,name='项目负责人权限--延期申请、编辑')
    group4.save()
    group5 = Group(id=5,name='产品负责人权限--编辑')
    group5.save()
    group6 = Group(id=6,name='测试负责人权限--编辑')
    group6.save()  
    group7 = Group(id=7,name='业务负责人权限--编辑')
    group7.save() 
    group8 = Group(id=8,name='运营负责人权限--编辑')
    group8.save() 
    group9 = Group(id=9,name='客服负责人权限--编辑')
    group9.save() 
    #auth_group_permissions
    group1.permissions.add(25)
    group1.permissions.add(26)
    group1.permissions.add(27)
    group1.permissions.add(35)
    group1.permissions.add(5)
    group2.permissions.add(23)
    group3.permissions.add(32)
    group4.permissions.add(34)
    group4.permissions.add(26)
    group5.permissions.add(26)
    group6.permissions.add(26)
    group7.permissions.add(26)
    group8.permissions.add(26)
    group9.permissions.add(26)
    #project_department
    depart1 = department(id=1,department='测试',isactived=1)
    depart1.save()
    depart2 = department(id=2,department='网站研发',isactived=1)
    depart2.save()
    depart3 = department(id=3,department='产品部',isactived=1)
    depart3.save()
    depart4 = department(id=4,department='客户端研发',isactived=1)
    depart4.save()
    depart5 = department(id=5,department='IT',isactived=1)
    depart5.save()
#    depart6 = department(id=6,department='院校事业',isactived=1)
#    depart6.save()
    depart7 = department(id=7,department='客服部',isactived=1)
    depart7.save()
    depart8 = department(id=8,department='市场部',isactived=1)
    depart8.save()
    depart9 = department(id=9,department='中小学事业部',isactived=1)
    depart9.save()
    depart10 = department(id=10,department='行政人事财务部',isactived=1)
    depart10.save()
    depart11 = department(id=11,department='管理部',isactived=1)
    depart11.save()
    depart12 = department(id=12,department='销售部',isactived=1)
    depart12.save()
    depart13 = department(id=13,department='项目研发部',isactived=1)
    depart13.save()
    depart100 = department(id=100,department='blank',isactived=1)
    depart100.save()   
    return HttpResponse("恭喜你,初始化数据成功~")

  
    
