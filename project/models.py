# coding=utf-8
from django.db import models

# Create your models here.

class department(models.Model):
    department= models.CharField(u'部门',max_length=20)
    isactived = models.BooleanField(max_length=1)
    
class user(models.Model):
    username= models.CharField(u'用户名',max_length=50)
    realname= models.CharField(u'真实姓名',max_length=50)
    password= models.CharField(u'密码',max_length=40)
    create_time = models.DateField()
    department = models.ForeignKey(department)
    Position_level = models.CharField(max_length=1,blank=True,default=0)
    isactived = models.BooleanField(max_length=1)
   
class project(models.Model):
    priority = models.SmallIntegerField(u'优先级',max_length=8)
    project = models.CharField(u'项目名称',max_length=100)
    status_p = models.CharField(u'项目状态',max_length=20)
    leader_p = models.ForeignKey(user)
    designer_p=models.ForeignKey(user, related_name='designer_p', blank=True, null=True)
    tester_p=models.ForeignKey(user, related_name='tester_p', blank=True, null=True)
    start_date = models.DateField(blank=True,null=True)
    expect_launch_date=models.DateField(blank=True,null=True)
    real_launch_date=models.DateField(blank=True,null=True)
    estimated_product_start_date = models.DateField(blank=True,null=True)
    estimated_product_end_date = models.DateField(blank=True,null=True)
    estimated_develop_start_date = models.DateField(blank=True,null=True)
    estimated_develop_end_date = models.DateField(blank=True,null=True)
    estimated_test_start_date = models.DateField(blank=True,null=True)
    estimated_test_end_date = models.DateField(blank=True,null=True)
    blueprint_p = models.CharField(max_length=100,blank=True,null=True)
    develop_plan_p = models.CharField(max_length=100,blank=True,null=True)
    test_plan_p = models.CharField(max_length=100,blank=True,null=True)
    test_case_p = models.CharField(max_length=100,blank=True,null=True)
    test_report_p = models.CharField(max_length=100,blank=True,null=True)
    isactived = models.BooleanField(max_length=1)

class project_user(models.Model):
    username = models.ForeignKey(user)
    project= models.ForeignKey(project)
    isactived = models.BooleanField(max_length=1)
    
class public_message(models.Model): 
    project = models.ForeignKey(project)  
    publisher=models.ForeignKey(user)
    content=models.CharField(u'公告内容',max_length=200)
    CHOICES = (  
        (u'notice',u'notice'),
        (u'message',u'message'), 
        
        )  
    type_p = models.CharField(max_length=30,choices=CHOICES)
    publication_date = models.DateField()
    delay_status = models.CharField(u'批准状态',max_length=10,null=True,blank=True)
    isactived = models.BooleanField(max_length=1)
        

class project_delay(models.Model):
    application = models.ForeignKey(user)
    project=models.ForeignKey(project)
    delay_to_date=models.DateField()
    apply_date=models.DateField()
    title = models.CharField(u'项目名称',max_length=100, blank=True, null=True)
    reason =models.CharField(u'拒绝理由',max_length=100, blank=True, null=True)
    result = models.CharField(u'状态',max_length=10,blank=True, null=True)
    review_date = models.DateField(blank=True,null=True)
    isactived = models.IntegerField(max_length=1,blank=True, null=True)


class project_user_message(models.Model):
    userid = models.ForeignKey(user)
    messageid = models.ForeignKey(public_message)
    project = models.ForeignKey(project)
    isactived = models.BooleanField(max_length=1)
