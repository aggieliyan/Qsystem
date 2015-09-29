# coding=utf-8
from redmine import Redmine
import json, time, datetime, os, uuid
from case.forms import fileBugForm
from django.http import HttpResponse
import case.models
from redmine.managers import ResourceNotFoundError
from Qsystem import settings

authKey = 'c3dbd70f0c3fe1a7c90432fab56dd9d298e48c8d' #具有管理员权限，可以访问redmine的API数据

def filebug(request):
    redmine = Redmine('http://192.168.3.221', key=authKey)
    web_dev = redmine.Group.get(41)
    client_dev = redmine.Group.get(67)
    dev_users = [web_dev.users, client_dev.users]
    dev_group = {}
    for item in dev_users:
        for user in item:
            dev_group[user.id] = user.name
    return HttpResponse(json.dumps(dev_group))    
def newbug(request, wid=''):
    if request.method == 'POST':
        uid = request.session['id'] #开bug前需要先关联key值，key值是redmine用户登录后，点击“我的帐号”,右边面板“API访问键”，点击“显示”，拷贝出来，加到case_redmine_key表中
        try:
            rkey = case.models.redmine_key.objects.get(uid=uid).key
        except:
            rs = {}
            rs['failed'] = True
            rs['message'] = "请联系李燕为您添加Redmine系统的Key值，才能正常开Bug~~"
            return HttpResponse(json.dumps(rs))         
        fb = fileBugForm(request.POST)
        if fb.is_valid():
            env = fb.cleaned_data['env']
            description = fb.cleaned_data['description']
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            description = u'使用'+env+u'环境'+today+u'版本：\r'+description
            fnames = fb.cleaned_data['attachment']
            fnames = fnames.split(',')
            uploads = []
            path = os.path.join(settings.MEDIA_ROOT,'bugAttachment/')
            for item in fnames:
                if item:
                    filename = item.split(":")[0]
                    fpath = path + item.split(":")[1]
                    uploads.append({'path': fpath, 'filename': filename})
            cid = fb.cleaned_data['cid']                
            ipid = cid if wid else case.models.category.objects.get(id=cid).redmine_proid 
            if not ipid:
                rs = {}
                rs['failed'] = True
                rs['message'] = "请先到产品管理页添加该项目所关联的Redmine项目id~~"
                return HttpResponse(json.dumps(rs))     
            redmine = Redmine('http://192.168.3.221', key=rkey)
            if '/newbug/' in request.path:
                issue = redmine.issue.get(wid) if wid else redmine.issue.new()
                issue.project_id = ipid
                issue.subject = fb.cleaned_data['subject']
                issue.tracker_id = fb.cleaned_data['itype']
                issue.description = description
                issue.status_id = fb.cleaned_data['status']
                issue.priority_id = fb.cleaned_data['PRI']
                issue.assigned_to_id = fb.cleaned_data['assign_to']
                issue.uploads = uploads
                issue.save() 
        if '/closewi/' in request.path:
            redmine = Redmine('http://192.168.3.221', key=rkey)
            try:
                issue = redmine.issue.get(wid)                
            except ResourceNotFoundError:
                return HttpResponse("can't find this wi, please close it by yourself~")    
            issue.status_id = 5            
            issue.save()                        
        return HttpResponse(issue.id)
def updatewi(request):
    buglist = request.GET
    updatewi = {}
    redmine = Redmine('http://192.168.3.221', key=authKey)
    results = []
    for tid, wid in buglist.items():
        try:
            issue = redmine.issue.get(wid)
        except ResourceNotFoundError:
            updatewi[wid] = "err"
        else:
            if issue.status.id != 1:
                updatewi[wid] = issue.status.id
            if issue.status.id == 5:
                results.append(case.models.result(testcase_id=tid, result='Pass', 
                                                  exec_date=datetime.datetime.now(), 
                                                  executor="Redmine更新", executorid="1", 
                                                  r_remark="#"+wid, isactived=1))
    case.models.result.objects.bulk_create(results)
    return HttpResponse(json.dumps(updatewi))
def getwi(request, wid):
    redmine = Redmine('http://192.168.3.221', key=authKey)
    try:
        issue = redmine.issue.get(wid)
    except ResourceNotFoundError:
        return HttpResponse('')
    else:            
        attachments = []
        for item in issue.attachments:
            attachments.append(item.filename)
        print list(issue.project)
        issueitem = {'id': issue.id, 'type': issue.tracker.id, 'status': issue.status.id, 
                     'subject': issue.subject, 'description': issue.description, 
                     'PRI': issue.priority.id, 'assign_to': issue.assigned_to.id, 
                     'uploads': attachments, 'cid': issue.project.id}
        return HttpResponse(json.dumps(issueitem))
#uploadify
#@csrf_exempt  
def uploadify_script(request):  
    ret="0"  
    file = request.FILES.get("Filedata",None)  
    print file.name
    if file:
        result,new_name=profile_upload(file)  
        if result:  
            ret="1"  
        else:  
            ret="2"                      
    res={'ret':ret,'save_name':new_name, 'old_name':file.name}  
    print json.dumps(res)
    return HttpResponse(json.dumps(res))        
      
def profile_upload(file):  
    '''''文件上传函数'''  
    if file:       
        path=os.path.join(settings.MEDIA_ROOT,'bugAttachment')  
        #file_name=str(uuid.uuid1())+".jpg"  
        file_name=str(uuid.uuid1())+'-'+file.name  
        #fname = os.path.join(settings.MEDIA_ROOT,filename)  
        path_file=os.path.join(path,file_name)  
        fp = open(path_file, 'wb')  
        for content in file.chunks():   
            fp.write(content)  
        fp.close()  
        return (True,file_name) #change  
    return (False,file_name)   #change  
      
    #用户管理-添加用户-删除附件  
     
#@csrf_exempt  
def profile_delte(request):  
    del_file=request.POST.get("delete_file",'')  
    if del_file:  
        path_file=os.path.join(settings.MEDIA_ROOT,'upload',del_file)  
        os.remove(path_file)  
        