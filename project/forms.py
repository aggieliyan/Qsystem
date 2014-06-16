# coding=utf-8
from django import forms

#login
from django.utils.translation import ugettext_lazy as _
from models import user
from models import department
import datetime

class RegisterForm(forms.Form):
    username=forms.CharField(label=_(u"用户名"),max_length=50)
    realname=forms.CharField(label=_(u'真实姓名'),max_length=50)
    password=forms.CharField(
        label=_(u"密码"),
        widget=forms.PasswordInput,
        max_length=40
    )
    confirmpassword=forms.CharField(
        label=_(u"确认密码"),
        widget=forms.PasswordInput,
        max_length=40
    )
    depart = forms.ModelChoiceField(
        queryset=department.objects.all().order_by('id'),
        required=True,
        label=u"所在部门",
        error_messages={'required': u'必选项'},
    )
    
    def clean_username(self):
        try:
            user.objects.get(username=self.cleaned_data['username'])
        except user.DoesNotExist:
            return self.cleaned__data['username']
        raise forms.ValidationError(u"用户名已存在，请选择别的用户名")

    def clean(self):
        if 'password' in self.clean_data and 'confirmpassword' in self.cleaned_data:
            if self.clean_data['password'] != self.cleaned_data['confirmpassword']:
                raise forms.ValidationError("You must type the same password each time")
        return self.cleaned_data
             
    def save(self):
        new_user = user.objects.create(username =self.cleaned_data['username'],
                                       realname =self.cleaned_data['realname'],
                                       password=self.cleaned_data['password'],
                                       depart=self.cleaned_data['depart'])
        return new_user
        
class UserForm(forms.Form):
    username = forms.CharField(label='账号：',max_length=100,required=True,error_messages={'required': u'必选项'})
    realname = forms.CharField(label='姓名：',max_length=100,required=True,error_messages={'required': u'必选项'})
    password = forms.CharField(label='密码：',max_length=100,widget=forms.PasswordInput(),required=True,error_messages={'required': u'必选项'})
    confirmpassword=forms.CharField(label="确认密码",max_length=100,widget=forms.PasswordInput(),required=True,error_messages={'required': u'必选项'}
    )
    departmentid = forms.CharField(label='部门：',max_length=100)
    # Create your views here.
    
    def save(self):
        new_user = user.objects.create(username =self.cleaned_data['username'],
                                       realname =self.cleaned_data['realname'],
                                       password=self.cleaned_data['password'],
                                       create_time=datetime.datetime.now(),
                                       department=department.objects.get(id=self.cleaned_data['departmentid']),isactived=0)
        return new_user

class LoginForm(forms.Form):
    username=forms.CharField(
        label=_(u"用户名"),
        max_length=20,
        error_messages={'required': u'请输入用户名'}
        )
    password=forms.CharField(
        label=_(u"密码"),
        required=False,
        widget=forms.PasswordInput,
        max_length=20
        )
    isautologin=forms.BooleanField(
        label=_(u"自动登录"),
        required=False
        )
#login


class ProjectForm(forms.Form):
	priority = forms.IntegerField(required=True, error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})
	pname = forms.CharField(required=True, error_messages={'required':u'项目名称不能为空'})
	status = forms.CharField(required=True, error_messages={'required':u'项目状态不能为空'})
	leader = forms.IntegerField(required=True, error_messages={'required':u'负责人不能为空'})
	designer = forms.IntegerField(required=False)
	tester = forms.IntegerField(required=False)
	startdate = forms.DateField(required=False)
	plandate=forms.DateField(required=False)
	psdate = forms.DateField(required=False)
	pedate = forms.DateField(required=False)
	dsdate = forms.DateField(required=False)
	dedate = forms.DateField(required=False)
	tsdate = forms.DateField(required=False)
	tedate = forms.DateField(required=False)
	ppath = forms.CharField(required=False)
	dppath = forms.CharField(required=False)
	tppath = forms.CharField(required=False)
	tcpath = forms.CharField(required=False)
	trpath = forms.CharField(required=False)
	relateduser = forms.CharField(required=False)

class changedesignForm(forms.Form):
	content=forms.CharField(required=True,error_messages={'invalid':u'变更内容不能为空'})
	dpath = forms.CharField(required=True,error_messages={'invalid':u'设计图地址不能为空'})
	changeid = forms.IntegerField(required=True)


class delayprojectForm(forms.Form):
	delay_date=forms.DateField(required=True,error_messages={'invalid':u'延期日期不能为空'})
	delay_reason = forms.CharField(required=True,error_messages={'invalid':u'延期理由不能为空'})
	delayid = forms.IntegerField(required=True)
class ProjectSearchForm(forms.Form):
	project=forms.CharField(required=False)
	start_date_s=forms.DateField(required=False)
	end_date_s=forms.DateField(required=False)
	status_p=forms.CharField(required=False)
	leader_p=forms.CharField(required=False)

class TestForm(forms.Form):
	delayid = forms.IntegerField(required=True,error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})
	reason = forms.CharField(required=True, error_messages={'required':u'项目名称不能为空'})

class ProusermessForm(forms.Form):
	usermessageid = forms.IntegerField(required=True,error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})
	
class MessageForm(forms.Form):
	messageid = forms.IntegerField(required=True,error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})
	
class NoticeForm(forms.Form):
	noticeid = forms.IntegerField(required=True,error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})

	
class Approveform(forms.Form):
	delayid1 = forms.IntegerField(required=True,error_messages={'required':u'优先级不能为空','invalid':u'优先级必须是正整数'})	