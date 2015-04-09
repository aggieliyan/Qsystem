# coding=utf-8
from django.db import models

# Create your models here.
RESULT_CHOICES = (
    ('P',u'PASS'),
    ('F',u'FAIL'),
    ('B',u'BLOCK'),
)
class category(models.Model):
	name = models.CharField(u'testcase项目名称', max_length=30)
	parent_id = models.IntegerField(u'父级id', max_length=20, blank=True, null=True)
	level = models.IntegerField(u'级数', max_length=3)
	createdate = models.DateTimeField(u'创建时间', blank=True, null=True)
	isactived = models.IntegerField(max_length=1)

class casemodule(models.Model):
	m_name = models.CharField(u'test模块名称', max_length=30)
	m_rank = models.IntegerField(u'编号', max_length=5)
	isactived = models.IntegerField(max_length=1)

class testcase(models.Model):
	category = models.ForeignKey(category)
	rank = models.IntegerField(u'编号', max_length=5)
	module = models.ForeignKey(casemodule, blank=True, null=True)
	precondition = models.CharField(u'前置条件', max_length=100, blank=True, null=True)
	action = models.CharField(u'输入/动作', max_length=100)
	output = models.CharField(u'期望输出', max_length=100)
	priority = models.IntegerField(u'优先级', max_length=1)
	author = models.CharField(u'本条用例作者', max_length=10)
	createdate = models.DateTimeField(u'创建时间', blank=True, null=True)
	t_remark = models.CharField(u'备注', blank=True, null=True, max_length=100)
	isactived = models.IntegerField(max_length=1)

class result(models.Model):
	testcase = models.ForeignKey(testcase)
	result = models.CharField(u'执行结果', choices = RESULT_CHOICES, max_length = 10)
	wi = models.CharField(u'WI', blank=True, null=True, max_length=8)
	exec_date = models.DateTimeField(u'执行时间', blank=True, null=True)
	executor = models.CharField(u'执行人', max_length=10, blank=True, null=True)
	executorid = models.IntegerField(u'执行人id', blank=False, null=False)
	r_remark = models.CharField(u'备注', blank=True, null=True, max_length=100)
	rounds = models.IntegerField(u'当前轮数', blank=True, null=True, max_length=2)
	isactived = models.IntegerField(max_length=1)