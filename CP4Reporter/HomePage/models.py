# -*- coding:utf-8 -*-
from django.db import models

# 经办人
class AssignModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# 报告人
class ReporterModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# 功能组接口类bug
class InterfaceModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# 组成员
class PersonModel(models.Model):
    lower_display_name = models.CharField(max_length = 20)
    lower_user_name = models.CharField(max_length = 20)

# 案例BUG
class CaseBugModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# no case bug
class NoCaseBugModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# 服务端BUG
class ServerBugModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# 前端BUG
class ClientBugModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()

# SOA BUG
class SOABugModel(models.Model):
    projectName = models.CharField(max_length = 50)
    issuekey = models.CharField(max_length = 20)
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    status = models.CharField(max_length = 20)
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateTimeField()
    UPDATED = models.DateTimeField()