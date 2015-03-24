# -*- coding:utf-8 -*-
from django.db import models

class Person(models.Model):
    lower_display_name = models.CharField(max_length = 20)
    lower_user_name = models.CharField(max_length = 20)

# 产品相关信息
class Products(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=20)
    product_key = models.CharField(max_length=10)

# 项目相关
class Projects(models.Model):
    project_name = models.CharField(max_length=50)
    project_target = models.TextField()
    project_scope = models.TextField()
    project_level = models.CharField(max_length=5)
    project_type = models.IntegerField()
    project_main_state = models.IntegerField() # 这个字段对应这个项目的状态(5表示已结项)
    project_id = models.IntegerField()    # 这个字段对应产品的ID
    project_state = models.IntegerField()


# 所有BUG
class AllIssues(models.Model):
    productID = models.IntegerField()
    productName = models.CharField(max_length=20)
    projectID = models.IntegerField()
    projectName = models.CharField(max_length = 50)
    MAIN_STATE = models.IntegerField()
    issuekey = models.CharField(max_length = 20)   # 这个字段用来链接到CP4的BUG明细上
    issueID = models.IntegerField()   # ji.ID
    SUMMARY = models.TextField(max_length=100)
    REPORTER = models.CharField(max_length = 20)
    ASSIGNEE = models.CharField(max_length = 20)
    PRIORITY = models.IntegerField()
    issuestatus = models.IntegerField()
    resolution = models.CharField(max_length = 20,blank = True,null = True)
    CREATED = models.DateField()
    UPDATED = models.DateField()
    reopenNums = models.IntegerField(default = 0)

# 所有重新打开的BUG
class AllReopenBugs(models.Model):
    issueID = models.CharField(max_length = 10)
    reopenNum = models.IntegerField()

