# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json,simplejson
from MainReport.models import *
from Util import myUtil
from django.template import RequestContext
import time

# 主页面
def index(request):
    products = Products.objects.all()
    return render_to_response('index.html',{"products":products})


# 根据产品获取项目
def get_projects_by_product(request):
    if request.method == "POST":
        product = request.POST['product']
        if product == u'所有产品':
            entrys = Projects.objects.all()
        else:
            product_entry = Products.objects.get(product_name=product)
            entrys = Projects.objects.filter(project_id = product_entry.product_id)
        return render_to_response('second.html',
            {
                'projects':entrys,
            }
        )
    else:
        return HttpResponse("error")

# 根据项目获取issues
def get_issues_by_project(request):
    if request.method == "POST":
        result = {}
        project = request.POST['project']
        if project == u'所有项目':
            entrys = AllIssues.objects.all().order_by('-CREATED')
        else:
            entrys = AllIssues.objects.filter(projectName__icontains = project).order_by('-CREATED')

        for entry in entrys:
            temp = {
                'openNums':0,
                'inProgressNums':0,
                'resolvedNums':0,
                'closedNums':0,
                'reopenNums':0,
                'topenNums':0,
                'treopenNums':0,
                'tclosedNums':0,
                'allNums':0,
            }
            if entry.projectName not in result:
                if entry.issuestatus == 1:
                    temp['openNums'] += 1
                elif entry.issuestatus == 3:
                    temp['inProgressNums'] += 1
                elif entry.issuestatus == 5:
                    temp['resolvedNums'] += 1
                elif entry.issuestatus == 6:
                    temp['closedNums'] += 1
                temp['reopenNums'] += entry.reopenNums
                temp['allNums'] = temp['openNums'] + temp['inProgressNums'] + temp['resolvedNums'] + temp['closedNums']
                result[entry.projectName] = temp

            else:
                if entry.issuestatus == 1:
                    result[entry.projectName]['openNums'] += 1
                if entry.issuestatus == 3:
                    result[entry.projectName]['inProgressNums'] += 1
                if entry.issuestatus == 5:
                    result[entry.projectName]['resolvedNums'] += 1
                if entry.issuestatus == 6:
                    result[entry.projectName]['closedNums'] += 1
                result[entry.projectName]['reopenNums'] += entry.reopenNums
                result[entry.projectName]['allNums'] += 1


        return render_to_response('issues.html',
            {
                'issues':result,
            },context_instance=RequestContext(request)
        )

# 初始化AllReopenBugs表
def init():
    # 设置reopenNums字段
    pass

# 设置项目重新打开BUG数字段的值
def set_pro_bug_reopen_nums():
    entrys = AllReopenBugs.objects.all()
    for en in entrys:
        issue_entrys = AllIssues.objects.filter(issueID = en.issueID)
        issue_entrys.update(reopenNums = en.reopenNum)

# 设置项目是否结束字段
def set_pro_is_closed(project_code,is_closed):
    pass


# 获取项目名称
def get_project_name():
    pass


# 当天日期
def nowTime():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))


# 获取今日新建、回退、关闭等BUG数
def get_today_data():
    pass

# 获取数据
def get_main_data():
    result = []
    _sql = '''
          select
              projectName,
              sum(case when `status`='Open' then 1 else 0 end) as 'OpenNums',
              sum(case when `status`='Closed' then 1 else 0 end) as 'ClosedNums',
              sum(case when `status`='Resolved' then 1 else 0 end) as 'ResolvedNums',
              sum(case when `status`='Reopened' then 1 else 0 end) as 'ReopenedNums',
              sum(case when `status`='InProgress' then 1 else 0 end) as 'InProgressNums',
              sum(reopenNums) as 'AllReopenNums',
              isClosed
          from
              mainreport_allbugs
          group by projectName
          ORDER BY CREATED DESC
    '''
    from django.db import connection,transaction
    cursor = connection.cursor()            #获得一个游标(cursor)对象
    #查询操作
    cursor.execute(_sql)
    raw = cursor.fetchall()                 #返回结果行 或使用 #raw = cursor.fetchall()
    today_data = get_today_data()
    for re in raw:
        temp = {
            'TOpenNums':0,
            'TClosedNums':0,
            'TResolvedNums':0,
            'TReopenedNums':0,
            'TInProgressNums':0,
            'OpenNums':0,
            'ClosedNums':0,
            'ResolvedNums':0,
            'ReopenedNums':0,
            'InProgressNums':0,
            'isClosed':0
        }
        if today_data:
            for data in today_data:
                if re[0] == data['projectName']:
                    temp['TOpenNums'] += data['TOpenNums']
                    temp['TClosedNums'] += data['TClosedNums']
                    temp['TResolvedNums'] += data['TResolvedNums']
                    temp['TReopenedNums'] += data['TReopenedNums']
                    temp['TInProgressNums'] += data['TInProgressNums']
                else:
                    pass
        if re[7] == 1:
            temp['projectName'] = re[0]+u'————(已结束)'
        else:
            temp['projectName'] = re[0]
        temp['OpenNums'] = re[1]
        temp['ClosedNums'] = re[2]
        temp['ResolvedNums'] = re[3]
        temp['ReopenedNums'] = re[4]
        temp['InProgressNums'] = re[5]
        temp['AllReopenNums'] = re[6]
        temp['isClosed'] = re[7]
        result.append(temp)
    return result







# 同步CP4数据库(由于消耗巨大,尽量少使用)
def sync_CP4_db(request):
    if request.method == 'POST':
        Person.objects.all().delete()
        Products.objects.all().delete()
        Projects.objects.all().delete()
        AllIssues.objects.all().delete()
        AllReopenBugs.objects.all().delete()

        # 获取远程数据库数据
        util = myUtil()

        for re in util.getQueryResult(util.getSQLStatement('static/sql/main.sql')):
            main = AllIssues(
                productID = re['productID'],
                productName = re['productName'],
                projectID = re['projectID'],
                projectName = re['projectName'],
                MAIN_STATE = re['MAIN_STATE'],
                issuekey = re['issuekey'],
                issueID = re['ID'],
                SUMMARY = re['SUMMARY'],
                REPORTER = re['REPORTER'],
                ASSIGNEE = re['ASSIGNEE'],
                PRIORITY = re['PRIORITY'],
                issuestatus = re['issuestatus'],
                resolution = re['RESOLUTION'],
                CREATED = re['CREATED'],
                UPDATED = re['UPDATED'],
            )
            main.save()

        for re in util.getQueryResult(util.getSQLStatement('static/sql/Products.sql')):
            products = Products(
                product_id = re['ID'],
                product_name = re['pname'],
                product_key = re['pkey'],
            )
            products.save()

        for re in util.getQueryResult(util.getSQLStatement('static/sql/Projects.sql')):
            projects = Projects(
                project_name = re['NAME'],
                project_target = re['TARGET'],
                project_scope = re['SCOPE'],
                project_level = re['LEVEL'],
                project_type = re['TYPE'],
                project_main_state = re['MAIN_STATE'],
                project_id = re['JIRA_PROJECT_ID'],
                project_state = re['STATE'],
            )
            projects.save()

        for re in util.getQueryResult(util.getSQLStatement('static/sql/user_in_group.sql')):
            users = Person(
                lower_display_name = re['lower_display_name'],
                lower_user_name = re['lower_user_name'],
            )
            users.save()

        for re in util.getQueryResult(util.getSQLStatement('static/sql/bug_reopen_nums.sql')):
            reopens = AllReopenBugs(
                issueID = re['issueId'],
                reopenNum = re['reopenNum'],
            )
            reopens.save()

        set_pro_bug_reopen_nums()

        return HttpResponse(simplejson.dumps(
            {
                'success':True,
                'message':'同步成功!',
            },ensure_ascii=False)
        )
    else:
        return HttpResponse(simplejson.dumps(
            {
                'success':False,
                'message':'请求错误!',
            },ensure_ascii=False)
        )