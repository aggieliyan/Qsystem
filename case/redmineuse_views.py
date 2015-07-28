# coding=utf-8
from redmine import Redmine
import json, time
from case.forms import fileBugForm
from django.http import HttpResponse
import case.models
from redmine.managers import ResourceNotFoundError

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
            return HttpResponse("请联系李燕为您添加Redmine系统的Key值，才能正常开Bug~~")         
        fb = fileBugForm(request.POST)
        if fb.is_valid():
            env = fb.cleaned_data['env']
            description = fb.cleaned_data['description']
            today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            description = '使用'+env+'环境'+today+'版本：\r'+description
            path = fb.cleaned_data['attachment']
            path = path.split(';')
            uploads = []
            for item in path:
                if item:
                    filename = item.split("\\")[-1]
                    uploads.append({'path': item, 'filename': filename})

            redmine = Redmine('http://192.168.3.221', key=rkey)
            if '/newbug/' in request.path:
                issue = redmine.issue.get(wid) if wid else redmine.issue.new()
                issue.project_id = 'vacation'
                issue.subject = fb.cleaned_data['subject']
                issue.tracker_id = fb.cleaned_data['type']
                issue.description = description
                issue.status_id = fb.cleaned_data['status']
                issue.priority_id = fb.cleaned_data['PRI']
                issue.assigned_to_id = fb.cleaned_data['assign_to']
                issue.uploads = uploads
                issue.save() 
        if '/closewi/' in request.path:
            redmine = Redmine('http://192.168.3.221', key=rkey)
            issue = redmine.issue.get(wid)
            issue.status_id = 5            
            issue.save()                        
        return HttpResponse(issue.id)
def updatewi(request, wids):
    if request.method == 'GET':
        if "wids":
            updatewi = {}
            redmine = Redmine('http://192.168.3.221', key=authKey)
            wids = wids.split('_')
            for wid in wids:
                if wid:
                    try:
                        issue = redmine.issue.get(wid)
                    except ResourceNotFoundError:
                        updatewi[wid] = "err"
                    else:
                        if issue.status.id != 1:
                            updatewi[wid] = issue.status.id
#                        if issue.status.id == 5:
#                            r = case.models.result.objects.filter(wi=wid).order_by("-id")[0]
#                            r.wi = ''
#                            r.save()
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
        issueitem = {'id': issue.id, 'type': issue.tracker.id, 'status': issue.status.id, 
                     'subject': issue.subject, 'description': issue.description, 
                     'PRI': issue.priority.id, 'assign_to': issue.assigned_to.id, 
                     'uploads': attachments}
        return HttpResponse(json.dumps(issueitem))

        