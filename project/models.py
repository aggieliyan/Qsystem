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
    Position_level = models.CharField(max_length=1,blank=True,default=3)
    isactived = models.BooleanField(max_length=1)
       
class project(models.Model):
    priority = models.SmallIntegerField(u'优先级',max_length=8)
    project = models.CharField(u'项目名称',max_length=100)
    type_p = models.CharField(u'项目类型',max_length=20)
    description = models.CharField(u'项目说明',max_length=1000,blank=True,null=True)
    status_p = models.CharField(u'项目状态',max_length=20)
    leader_p = models.ForeignKey(user)
    designer_p = models.ForeignKey(user, related_name="designer_p",blank=True,null=True)
    tester_p = models.ForeignKey(user, related_name="tester_p",blank=True,null=True)
    business_man = models.ForeignKey(user, related_name="business_man",blank=True,null=True)
    operator_p = models.ForeignKey(user, related_name="operator_p",blank=True,null=True)
    customer_service = models.ForeignKey(user, related_name="customer_service",blank=True,null=True)
    start_date = models.DateField(blank=True,null=True)
    expect_launch_date = models.DateField(blank=True,null=True)
    real_launch_date = models.DateField(blank=True,null=True)
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
    praise_p = models.SmallIntegerField(max_length=8,default=0)
    remark_p = models.TextField(u'备注', max_length=10000,blank=True,null=True)

class project_user(models.Model):
    username = models.ForeignKey(user)
    project= models.ForeignKey(project)
    roles = models.IntegerField()
    #roles 0 产品
    #      1 开发
    #      2 测试
    #      3 业务
    #      4 运营
    #      5 客服
    isactived = models.BooleanField(max_length=1)
    
class public_message(models.Model): 
    project = models.IntegerField()  
    publisher=models.IntegerField()
    content=models.CharField(u'公告内容',max_length=2500)
    CHOICES = (  
        (u'notice',u'notice'),
        (u'message',u'message'), 
        
        )  
    type_p = models.CharField(max_length=30,choices=CHOICES)
    publication_date = models.DateField()
    delay_status = models.CharField(u'批准状态',max_length=10,null=True,blank=True)
    isactived = models.IntegerField(max_length=1)
        

class project_delay(models.Model):
    application = models.ForeignKey(user)
    project=models.ForeignKey(project)
    delay_to_date=models.DateField()
    apply_date=models.DateField()
    title = models.CharField(u'项目名称',max_length=100, blank=True, null=True)
    reason =models.CharField(u'拒绝理由',max_length=500, blank=True, null=True)
    result = models.CharField(u'状态',max_length=10,blank=True, null=True)
    review_date = models.DateField(blank=True,null=True)
    isactived = models.IntegerField(max_length=1,blank=True, null=True)


class project_user_message(models.Model):
    userid = models.ForeignKey(user)
    messageid = models.ForeignKey(public_message)
    project = models.ForeignKey(project)
    isactived = models.BooleanField(max_length=1)
    

class project_statistics(models.Model):
    project_id = models.IntegerField(max_length=9999999,blank=False, null=False)
    item = models.CharField(u'统计项', max_length=1000)
    db = models.CharField(u'使用哪个库',max_length=50)
    sql = models.TextField(u'查询语句', max_length=21000)
    total = models.TextField(max_length=9999999,blank=True, null=True) 
    is_graph = models.BooleanField(u'是否画图')   
    is_editable = models.BooleanField(u'是否可编辑')
    isactived = models.IntegerField(max_length=1, blank=False, null=False, default=1) 

class project_feedback(models.Model):
    project= models.ForeignKey(project)
    feedback_member = models.ForeignKey(user)
    content = models.CharField(u'反馈内容', max_length=700)
    feedback_date = models.DateTimeField(blank=True,null=True)

class project_feedback_comment(models.Model):
    feedbackid = models.ForeignKey(project_feedback)
    feedback_member_c = models.ForeignKey(user)
    comment = models.CharField(u'回复内容', max_length=700)
    feedback_date_c = models.DateTimeField(blank=True,null=True)

class project_operator_bussniess_message(models.Model):
    userid = models.ForeignKey(user)
    project = models.ForeignKey(project)
    user_type = models.CharField(u'人员类型',max_length=20)
    title = models.CharField(u'项目名称',max_length=100, blank=True, null=True)
    status = models.CharField(u'状态',max_length=10,blank=True, null=True)
    publication_date = models.DateField()    
    confirm_design_date = models.DateField(blank=True, null=True)
    check_date = models.DateField(blank=True, null=True)
    isactived = models.IntegerField(max_length=1,blank=True, null=True) 

#统计信息相关表
class module(models.Model):
    module_name= models.CharField(u'模块名称',max_length=20)
    isactived = models.BooleanField()

class project_module(models.Model):
    project = models.ForeignKey(project)
    module = models.ForeignKey(module)
    isactived = models.BooleanField()

class project_statistics_result(models.Model):
    project = models.ForeignKey(project)
    sql = models.ForeignKey(project_statistics)
    date = models.DateField(u'统计日期')
    statistical_result = models.IntegerField(u'统计结果', max_length=10)
    isactived = models.BooleanField()
