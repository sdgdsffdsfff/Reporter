# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from suds.client import Client as sudsclient
import time
from Util import myUtil
from models import *
from time import timezone
import datetime
from PeopleConfig import peopleConfig

__author__ = 'kiven'

def index(request):
    proInfo = {}
    personInfo = {}

    util = myUtil()
    sql = util.getSQLStatement('static/SQL/cpm.sql')
    sql_cpms = util.getSQLStatement('static/SQL/cpms.sql')
    sql_nocpm = util.getSQLStatement('static/SQL/nocpm.sql')



    result = util.getQueryResult(sql)
    result_cpms = util.getQueryResult(sql_cpms)
    result_nocpm = util.getQueryResult(sql_nocpm)



    # 三种SQL情况下的所有issue状态为BUG的放入一个列表中
    if result_cpms:
        for i in range(len(result_cpms)):
            result.append(result_cpms[i])
    if result_nocpm:
        for j in range(len(result_nocpm)):
            result.append(result_nocpm[j])

    # 获取所有项目名
    pName = util.getProName(result)

    # 获取状态以及各状态BUG数量
    allBugNum = 0
    inprogessNum = 0
    openBugNum = 0
    closedBugNum = 0
    resolvedBugNum = 0
    todayOpenBugNum = 0
    todayReopenBugNum =0
    todayCloseBugNum = 0

    for i in range(len(pName)):
        status = util.getProStatus(result,pName[i])
        proInfo[pName[i]] = status
        # 所有项目的所有BUG总数
        allBugNum += status['total']
        openBugNum += status['Open']
        inprogessNum += status['InProgress']
        closedBugNum += status['Closed']
        resolvedBugNum += status['Resolved']
        todayOpenBugNum += status['todayOpen']
        todayReopenBugNum += status['todayReopen']
        todayCloseBugNum += status['todayClose']
        # status.append(util.getProStatus(result,pName[i]))



    # 个人BUG各状态数量
    allStatusNum = openStatusNum = closeStatusNum = resolvedStatusNum = inprogessStatusNum = 0

    sql_getperson = util.getSQLStatement('static/SQL/getPerson.sql')
    result_getperson = util.getQueryResult(sql_getperson)
    personName = util.getPerson(result_getperson)
    for k in range(len(personName)):
        status = util.getBugStatus(result_getperson,personName[k])
        personInfo[personName[k]] = status
        allStatusNum += status['total']
        openStatusNum += status['open']
        closeStatusNum += status['closed']
        resolvedStatusNum += status['resolved']
        inprogessStatusNum += status['inprogess']



    #
    return render_to_response('index.html',{
        'proInfo':proInfo,
        'allBugNum':allBugNum,
        'openBugNum':openBugNum,
        'inprogressNum':inprogessNum,
        'closedBugNum':closedBugNum,
        'resolvedBugNum':resolvedBugNum,
        'todayOpenBugNum':todayOpenBugNum,
        'todayReopenBugNum':todayReopenBugNum,
        'todayCloseBugNum':todayCloseBugNum,

        'personInfo':personInfo,
        'allStatusNum':allStatusNum,
        'openStatusNum':openStatusNum,
        'closeStatusNum':closeStatusNum,
        'resolvedStatusNum':resolvedStatusNum,
        'inprogessStatusNum':inprogessStatusNum,
    })

# 返回组内所有成员的显示名称
def personDisplayName():
    results = []
    # 检索所有的对象
    entrys = PersonModel.objects.all()
    for p in entrys:
        results.append(p.lower_display_name)
    return results

# 返回组内所有成员的名称
def personUseryName():
    results = []
    # 检索所有的对象
    entrys = PersonModel.objects.all()
    for p in entrys:
        results.append(p.lower_user_name)
    return results


'''获取每个成员的各类状态的BUG数或经办的项目
@:param pName : 成员名
@:param bStatus : BUG状态 default = All
@:param type : 类型(经办人or报告人)---------废弃
'''
def getEveryData(pName,**args):
    if args:
        for k in args:
            entrys = ReporterModel.objects.filter(REPORTER = pName,status = args[k])
    else:
        entrys = ReporterModel.objects.filter(REPORTER = pName)
    i = len(entrys)
    return i
    # return HttpResponse(everyData,content_type="application/json" )

'''返回项目名称
'''
def getProName():
    result = []
    entrys = ReporterModel.objects.all()
    for p in entrys:
        pn = p.projectName
        if not pn in result:
            result.append(pn)
    return result

'''获取每个项目下的BUG数
'''
def getProData(proName,**args):
    # BUG所属server端或soa端或client端
    typeNum = ['server','soa']
    # 每一端BUG的数量
    result = {
        'client':0,
        'server':0,
        'soa':0,
        'all':0,
    }

    for k in args:
        all = ReporterModel.objects.filter(projectName = proName,status = args[k])
        for bug_type in typeNum:
            entrys = ReporterModel.objects.filter(projectName = proName,ASSIGNEE__in = peopleConfig(bug_type),status = args[k])
            for i in result:
                if i == bug_type:
                    result[i] = len(entrys)
    result['client'] = len(all) - result['server'] - result['soa']
    result['all'] = len(all)

    return result

# 邮件发送接口
def send_email(request):
    if request.method=="POST" and request.POST['mailContent']:
        sudsclient_email=sudsclient("http://192.168.81.123/SendMail/SendMail.asmx?wsdl")
        try:
            sudsclient_email.service.SendMailWithHtml2("shen_jl@ctrip.com",u"金融测试组（功能）项目BUG统计",request.POST['mailContent'],"shen_jl@ctrip.com")
        except:
            return HttpResponse(u"发送失败!")
        return HttpResponse(u'发送成功!')


# 当天日期
def todayTime():
    now = datetime.datetime.now()
    start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
    return start

# 当天日期
def nowTime():
    return time.strftime('%Y-%m-%d',time.localtime(time.time()))

'''获取过去任意一天日期
@:param int类型,距今天相差的天数
'''
def anyDay(delta):
    today = datetime.date.today()
    anyday = today - datetime.timedelta(days=delta)
    return anyday

# 字典按键排序
def sortedDictValues(adict):
    result = []
    keys = adict.keys()
    keys.sort()
    for key in keys:
        tmp = {}
        tmp['time'] = key
        tmp['num'] = adict[key]
        result.append(tmp)
    return result

'''获取历史每日新建BUG数量
@:param days : 统计多长时间内的数据,默认为一周
@:param reporter : BUG提交人的名字
'''
def getEveryDayBugOpenData(days = 'week',reporter = None):
    result = {}
    howDays = {
        'week':7,
        'month':30,
        'quarter':90,
        'halfyear':183,
        'year':365,
    }

    for i in range(howDays[days]):
        thatDay = anyDay(i)
        if not reporter:
            entrys = ReporterModel.objects.filter(CREATED__startswith = thatDay)
        else:
            entrys = ReporterModel.objects.filter(REPORTER = reporter,CREATED__startswith = thatDay)
        result[thatDay] = len(entrys)

    return result

'''获取历史每日关闭BUG数量
@:param days : 统计多长时间内的数据,默认为一周
@:param reporter : BUG提交人的名字
'''
def getEveryDayBugClosedData(days = 'week',reporter = None):
    result = {}
    howDays = {
        'week':7,
        'month':30,
        'quarter':90,
        'halfyear':183,
        'year':365,
    }

    for i in range(howDays[days]):
        thatDay = anyDay(i)
        if not reporter:
            entrys = ReporterModel.objects.filter(UPDATED__startswith = thatDay,status = 'Closed')
        else:
            entrys = ReporterModel.objects.filter(REPORTER = reporter,UPDATED__startswith = thatDay)
        result[thatDay] = len(entrys)

    return result

# 获取趋势图
def getChart(request):
    if request.method=="POST" and request.POST['dataType']:
        dataType = request.POST['dataType']
        '''BUG每日趋势'''
        every_week_bug_open = sortedDictValues(getEveryDayBugOpenData(dataType))
        every_week_bug_closed = sortedDictValues(getEveryDayBugClosedData(dataType))

        return render_to_response('chart.html',{
            'every_week_bug_open':every_week_bug_open,
            'every_week_bug_closed':every_week_bug_closed,
            'dataType':dataType}
        )
    else:
        return HttpResponse("参数异常!")


# 经办项目统计
def getProjectPage(request):
    results = []
    entrys = AssignModel.objects.all()

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED

        results.append(tmp)

    return render_to_response('AllProPage.html',{
        'results':results
    })


# mainReport模版
def mainReport(request):

    '''
    pb = {'pName':{'open':xx,'inprogress':xx,'resolved':xx,'closed':xxx,'all':xxx,'link':'/personal.html/'}}
    '''
    '''########################################################################################'''
    # 组员与BUG
    pb = {}
    all = {
            'Open':0,
            'Reopened':0,
            'InProgress':0,
            'Resolved':0,
            'Closed':0,
            'CaseBug':0,
            'NoCaseBug':0,
            'All':0,
        }
    pNames = personDisplayName()
    # 某个人的所有信息
    for p in pNames:
        case_entrys = ReporterModel.objects.filter(REPORTER = p,ASSIGNEE__in = peopleConfig('case_bug'))
        nocase_entrys = NoCaseBugModel.objects.filter(REPORTER = p)
        case_num = len(case_entrys)
        nocase_num = len(nocase_entrys)

        b = {
            'Open':0,
            'Reopened':0,
            'InProgress':0,
            'Resolved':0,
            'Closed':0,
            'CaseBug':0,
            'NoCaseBug':0,
            'All':0,
        }
        b['CaseBug'] = case_num
        all['CaseBug'] += case_num
        b['NoCaseBug'] = nocase_num
        all['NoCaseBug'] += nocase_num

        b['Open'] = getEveryData(p,status = 'Open')
        all['Open'] += b['Open']
        b['Reopened'] = getEveryData(p,status = 'Reopened')
        all['Reopened'] += b['Reopened']
        b['InProgress'] = getEveryData(p,status = 'In Progress')
        all['InProgress'] += b['InProgress']
        b['Resolved'] = getEveryData(p,status = 'Resolved')
        all['Resolved'] += b['Resolved']
        b['Closed'] = getEveryData(p,status = 'Closed')
        all['Closed'] += b['Closed']
        b['All'] = b['Open'] + b['Reopened'] + b['InProgress'] + b['Resolved'] + b['Closed']
        all['All'] += b['All']
        pb[p] = b
    '''########################################################################################'''
    # 项目BUG
    pn = {}
    pnAll = {
        'Open':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'Reopened':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'InProgress':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'Resolved':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'Closed':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'TodayOpen':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'TodayReOpen':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'TodayClosed':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
        'CaseBug':0,
        'NoCaseBug':0,
        'InterfaceBug':0,
        'All':{
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        },
    }
    proNames = getProName()
    for p in proNames:

        # BUG所属server端或soa端或client端
        typeNum = ['server','soa']
        # 每一端BUG的数量
        t_o_result = {
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        }
        t_r_result = {
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        }
        t_c_result = {
            'client':0,
            'server':0,
            'soa':0,
            'all':0,
        }

        t_o_entrys_all = ReporterModel.objects.filter(projectName = p,CREATED__startswith = nowTime())
        t_r_entrys_all = ReporterModel.objects.filter(projectName = p,status = 'Reopened',UPDATED__startswith = nowTime())
        t_c_entrys_all = ReporterModel.objects.filter(projectName = p,status = 'Closed',UPDATED__startswith = nowTime())
        # t_o_result
        for bug_type in typeNum:
            entrys = ReporterModel.objects.filter(projectName = p,ASSIGNEE__in = peopleConfig(bug_type),CREATED__startswith = nowTime())
            for i in t_o_result:
                if i == bug_type:
                    t_o_result[i] = len(entrys)
        # t_r_result
        for bug_type in typeNum:
            entrys = ReporterModel.objects.filter(projectName = p,ASSIGNEE__in = peopleConfig(bug_type),status = 'Reopened',UPDATED__startswith = nowTime())
            for i in t_r_result:
                if i == bug_type:
                    t_r_result[i] = len(entrys)
        # t_c_result
        for bug_type in typeNum:
            entrys = ReporterModel.objects.filter(projectName = p,ASSIGNEE__in = peopleConfig(bug_type),status = 'Closed',UPDATED__startswith = nowTime())
            for i in t_c_result:
                if i == bug_type:
                    t_c_result[i] = len(entrys)

        t_o_result['client'] = len(t_o_entrys_all) - t_o_result['server'] - t_o_result['soa']
        t_r_result['client'] = len(t_r_entrys_all) - t_r_result['server'] - t_r_result['soa']
        t_c_result['client'] = len(t_c_entrys_all) - t_c_result['server'] - t_c_result['soa']

        t_o_result['all'] = len(t_o_entrys_all)
        t_r_result['all'] = len(t_r_entrys_all)
        t_c_result['all'] = len(t_c_entrys_all)

        # 今日数据
        # t_o_entrys = ReporterModel.objects.filter(projectName = p,CREATED__startswith = nowTime() )
        # t_r_entrys = ReporterModel.objects.filter(projectName = p,status = 'Reopened',UPDATED__startswith = nowTime())
        # t_c_entrys = ReporterModel.objects.filter(projectName = p,status = 'Closed',UPDATED__startswith = nowTime())
        case_entrys = ReporterModel.objects.filter(projectName = p,ASSIGNEE__in = peopleConfig('case_bug'))

        interface_entrys = InterfaceModel.objects.filter(projectName = p)

        nocase_entrys = NoCaseBugModel.objects.filter(projectName = p)

        case_num = len(case_entrys)
        nocase_num = len(nocase_entrys)
        interface_num = len(interface_entrys)

        b = {
            'Open':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'Reopened':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'InProgress':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'Resolved':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'Closed':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'TodayOpen':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'TodayReOpen':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'TodayClosed':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
            'CaseBug':0,
            'NoCaseBug':0,
            'InterfaceBug':0,
            'All':{
                'client':0,
                'server':0,
                'soa':0,
                'all':0,
            },
        }

        b['InterfaceBug'] =interface_num
        pnAll['InterfaceBug'] += interface_num

        b['CaseBug'] = case_num
        pnAll['CaseBug'] += case_num
        b['NoCaseBug'] = nocase_num
        pnAll['NoCaseBug'] += nocase_num

        b['Open'] = getProData(p,status = 'Open')
        pnAll['Open']['all'] += b['Open']['all']
        pnAll['Open']['client'] += b['Open']['client']
        pnAll['Open']['server'] += b['Open']['server']
        pnAll['Open']['soa'] += b['Open']['soa']

        b['Reopened'] = getProData(p,status = 'Reopened')
        pnAll['Reopened']['all'] += b['Reopened']['all']
        pnAll['Reopened']['client'] += b['Reopened']['client']
        pnAll['Reopened']['server'] += b['Reopened']['server']
        pnAll['Reopened']['soa'] += b['Reopened']['soa']

        b['InProgress'] = getProData(p,status = 'In Progress')
        pnAll['InProgress']['all'] += b['InProgress']['all']
        pnAll['InProgress']['client'] += b['InProgress']['client']
        pnAll['InProgress']['server'] += b['InProgress']['server']
        pnAll['InProgress']['soa'] += b['InProgress']['soa']

        b['Resolved'] = getProData(p,status = 'Resolved')
        pnAll['Resolved']['all'] += b['Resolved']['all']
        pnAll['Resolved']['client'] += b['Resolved']['client']
        pnAll['Resolved']['server'] += b['Resolved']['server']
        pnAll['Resolved']['soa'] += b['Resolved']['soa']


        b['Closed'] = getProData(p,status = 'Closed')
        pnAll['Closed']['all'] += b['Closed']['all']
        pnAll['Closed']['client'] += b['Closed']['client']
        pnAll['Closed']['server'] += b['Closed']['server']
        pnAll['Closed']['soa'] += b['Closed']['soa']

        b['TodayOpen'] = t_o_result
        b['TodayReOpen'] = t_r_result
        b['TodayClosed'] = t_c_result


        pnAll['TodayOpen']['all'] += t_o_result['all']
        pnAll['TodayOpen']['client'] += t_o_result['client']
        pnAll['TodayOpen']['server'] += t_o_result['server']
        pnAll['TodayOpen']['soa'] += t_o_result['soa']

        pnAll['TodayReOpen']['all'] += t_r_result['all']
        pnAll['TodayReOpen']['client'] += t_r_result['client']
        pnAll['TodayReOpen']['server'] += t_r_result['server']
        pnAll['TodayReOpen']['soa'] += t_r_result['soa']

        pnAll['TodayClosed']['all'] += t_c_result['all']
        pnAll['TodayClosed']['client'] += t_c_result['client']
        pnAll['TodayClosed']['server'] += t_c_result['server']
        pnAll['TodayClosed']['soa'] += t_c_result['soa']

        b['All']['all'] = b['Open']['all'] + b['Reopened']['all'] + b['InProgress']['all'] + b['Resolved']['all'] + b['Closed']['all']
        b['All']['client'] = b['Open']['client'] + b['Reopened']['client'] + b['InProgress']['client'] + b['Resolved']['client'] + b['Closed']['client']
        b['All']['server'] = b['Open']['server'] + b['Reopened']['server'] + b['InProgress']['server'] + b['Resolved']['server'] + b['Closed']['server']
        b['All']['soa'] = b['Open']['soa'] + b['Reopened']['soa'] + b['InProgress']['soa'] + b['Resolved']['soa'] + b['Closed']['soa']
        pnAll['All']['all'] += b['All']['all']
        pnAll['All']['client'] += b['All']['client']
        pnAll['All']['server'] += b['All']['server']
        pnAll['All']['soa'] += b['All']['soa']

        if p!="":
           pn[p] = b
        else:
           pn[u'未规划项目'] = b



    return render_to_response('MainReport.html',{
        'pb':pb,
        'pn':pn,
        'pnall':pnAll,
        'all':all,

    }
    )



'''########################################################################################'''
# 个人页
def personalBugPage(request):
    results = []
    pName = request.GET['pName']
    entrys = ReporterModel.objects.filter(REPORTER = pName)

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED
        tmp['UPDATED'] = k.UPDATED

        results.append(tmp)

    return render_to_response('PersonalBug.html',{
        'pName':pName,
        'results':results
    })

# 项目页
def projectBugPage(request):
    results = []
    proName = request.GET['proName']
    if proName == u'未规划项目':
        proName = ''
    entrys = ReporterModel.objects.filter(projectName = proName)

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED
        tmp['UPDATED'] = k.UPDATED

        results.append(tmp)

    if proName == '':
        proName = u'未规划项目'

    return render_to_response('ProjectBug.html',{
        'proName':proName,
        'results':results
    })

# 所有BUG页
def allBugPage(request):
    results = []
    entrys = ReporterModel.objects.all()

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED

        results.append(tmp)

    return render_to_response('AllBugPage.html',{
        'results':results
    })

# ----------------------------------各BUG状态数字下的链接start------------------------------------------
# 每个组员对应各状态的BUG详细页
def personalBugDetails(request):
    results = []
    pName = request.GET['pName']
    status = request.GET['status']
    # 总计里的
    if pName == 'all':
        if status == 'TodayOpen':
            entrys = ReporterModel.objects.filter(CREATED__startswith = nowTime())
        elif status == 'TodayReOpen':
            entrys = ReporterModel.objects.filter(status = 'Reopened',UPDATED__startswith = nowTime())
        elif status == 'TodayClosed':
            entrys = ReporterModel.objects.filter(status = 'Closed',UPDATED__startswith = nowTime())
        elif status == 'CaseBug':
            entrys = ReporterModel.objects.filter(ASSIGNEE__in = peopleConfig('case_bug'))
        elif status == 'NoCaseBug':
            entrys = NoCaseBugModel.objects.filter()
        else:
            entrys = ReporterModel.objects.filter(status = status)
    else:
        if status == 'TodayOpen':
            entrys = ReporterModel.objects.filter(REPORTER = pName,CREATED__startswith = nowTime())
        elif status == 'TodayReOpen':
            entrys = ReporterModel.objects.filter(REPORTER = pName,status = 'Reopened',UPDATED__startswith = nowTime())
        elif status == 'TodayClosed':
            entrys = ReporterModel.objects.filter(REPORTER = pName,status = 'Closed',UPDATED__startswith = nowTime())
        elif status == 'CaseBug':
            entrys = ReporterModel.objects.filter(REPORTER = pName,ASSIGNEE__in = peopleConfig('case_bug'))
        elif status == 'NoCaseBug':
            entrys = NoCaseBugModel.objects.filter(REPORTER = pName)
        else:
            entrys = ReporterModel.objects.filter(REPORTER = pName,status = status)

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED

        results.append(tmp)

    return render_to_response('BugDetails_other.html',{
        'pName':pName,
        'status':status,
        'results':results
    })

# 各项目对应的各状态的BUG详细页
def bugDetails(request):
    results = []
    proName = request.GET['proName']
    status = request.GET['status']
    if proName == u'未规划项目':
        proName = ''
    # 总计里的
    if proName == 'all':
        entrys = ReporterModel.objects.filter(status = status)
    else:
        entrys = ReporterModel.objects.filter(projectName = proName,status = status)

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED

        results.append(tmp)

    if proName == '':
        proName = u'未规划项目'

    return render_to_response('BugDetails.html',{
        'proName':proName,
        'status':status,
        'results':results
    })

# 各项目今日新建、今日回退、今日关闭、案例BUG、NoCaseBug详细页
def todayBugDetails(request):
    typeNum = ['server','soa']
    results = []
    proName = request.GET['proName']
    status = request.GET['status']
    if proName == u'未规划项目':
        proName = ''

    # 总计里的
    if proName == 'all':
        if status == 'TodayOpen':
            entrys = ReporterModel.objects.filter(CREATED__startswith = nowTime())
        elif status == 'TodayReOpen':
            entrys = ReporterModel.objects.filter(status = 'Reopened',UPDATED__startswith = nowTime())
        elif status == 'TodayClosed':
            entrys = ReporterModel.objects.filter(status = 'Closed',UPDATED__startswith = nowTime())
        elif status == 'CaseBug':
            entrys = ReporterModel.objects.filter(ASSIGNEE__in = peopleConfig('case_bug'))
        elif status == 'NoCaseBug':
            entrys = NoCaseBugModel.objects.all()
        elif status == 'interfaceBug':
            entrys = InterfaceModel.objects.all()
    else:
        if status == 'TodayOpen':
            entrys = ReporterModel.objects.filter(projectName = proName,CREATED__startswith = nowTime())
        elif status == 'TodayReOpen':
            entrys = ReporterModel.objects.filter(projectName = proName,status = 'Reopened',UPDATED__startswith = nowTime())
        elif status == 'TodayClosed':
            entrys = ReporterModel.objects.filter(projectName = proName,status = 'Closed',UPDATED__startswith = nowTime())
        elif status == 'CaseBug':
            entrys = ReporterModel.objects.filter(projectName = proName,ASSIGNEE__in = peopleConfig('case_bug'))
        elif status == 'NoCaseBug':
            entrys = NoCaseBugModel.objects.filter(projectName = proName)
        elif status == 'interfaceBug':
            entrys = InterfaceModel.objects.filter(projectName = proName)

    for k in entrys:
        tmp = {}
        tmp['id'] = k.id
        tmp['projectName'] = k.projectName
        tmp['issuekey'] = k.issuekey
        tmp['SUMMARY'] = k.SUMMARY
        tmp['REPORTER'] = k.REPORTER
        tmp['ASSIGNEE'] = k.ASSIGNEE
        tmp['PRIORITY'] = k.PRIORITY
        tmp['status'] = k.status
        tmp['CREATED'] = k.CREATED

        results.append(tmp)

    if proName == '':
        proName = u'未规划项目'

    return render_to_response('BugDetails_other.html',{
        'proName':proName,
        'status':status,
        'results':results
    })
# ----------------------------------各BUG状态数字下的链接over------------------------------------------

'''########################################################################################'''

# 数据库同步页
def syncDb(request):
    return render_to_response('SyncDB.html')

# 同步本地数据库
def syncCP4DB(request):
    if request.method=="POST":
        # 清空表
        PersonModel.objects.all().delete()
        ReporterModel.objects.all().delete()
        AssignModel.objects.all().delete()
        CaseBugModel.objects.all().delete()
        NoCaseBugModel.objects.all().delete()
        ServerBugModel.objects.all().delete()
        ClientBugModel.objects.all().delete()
        SOABugModel.objects.all().delete()
        InterfaceModel.objects.all().delete()

        ass_result = []
        rep_result = []
        nocasebug_result = []
        interface_result = []

        # 获取远程数据库数据
        util = myUtil()



        # 所有组内成员
        sql = "SELECT cu.lower_display_name,cu.lower_user_name FROM cwd_user cu LEFT JOIN cwd_membership cms ON cu.ID = cms.child_id where cms.parent_id = 29988;"
        result = util.getQueryResult(sql)

        ass1_sql = util.getSQLStatement('static/SQL/assignee1.sql')
        ass2_sql = util.getSQLStatement('static/SQL/assignee2.sql')
        ass3_sql = util.getSQLStatement('static/SQL/assignee3.sql')
        rep1_sql = util.getSQLStatement('static/SQL/reporter1.sql')
        rep2_sql = util.getSQLStatement('static/SQL/reporter2.sql')
        rep3_sql = util.getSQLStatement('static/SQL/reporter3.sql')
        nocasebug1_sql = util.getSQLStatement('static/SQL/nocasebug1.sql')
        nocasebug2_sql = util.getSQLStatement('static/SQL/nocasebug2.sql')
        nocasebug3_sql = util.getSQLStatement('static/SQL/nocasebug3.sql')
        interface_sql1 = util.getSQLStatement('static/SQL/interface_bug1.sql')
        interface_sql2 = util.getSQLStatement('static/SQL/interface_bug2.sql')
        interface_sql3 = util.getSQLStatement('static/SQL/interface_bug3.sql')
        ass1_result = util.getQueryResult(ass1_sql)
        rep1_result = util.getQueryResult(rep1_sql)
        ass2_result = util.getQueryResult(ass2_sql)
        ass3_result = util.getQueryResult(ass3_sql)
        rep2_result = util.getQueryResult(rep2_sql)
        rep3_result = util.getQueryResult(rep3_sql)
        interface1_result = util.getQueryResult(interface_sql1)
        interface2_result = util.getQueryResult(interface_sql2)
        interface3_result = util.getQueryResult(interface_sql3)

        # ===================================================================
        # no case bug
        nocasebug1_result = util.getQueryResult(nocasebug1_sql)
        nocasebug2_result = util.getQueryResult(nocasebug2_sql)
        nocasebug3_result = util.getQueryResult(nocasebug3_sql)

        for i in range(len(interface1_result)):
            interface_result.append(interface1_result[i])
        for i in range(len(interface2_result)):
            interface_result.append(interface2_result[i])
        for i in range(len(interface3_result)):
            interface_result.append(interface3_result[i])

        for i in range(len(interface_result)):
            interface = InterfaceModel(
                projectName = interface_result[i]['projectName'],
                issuekey = interface_result[i]['issuekey'],
                SUMMARY = interface_result[i]['SUMMARY'],
                REPORTER = interface_result[i]['REPORTER'],
                ASSIGNEE = interface_result[i]['ASSIGNEE'],
                PRIORITY = interface_result[i]['PRIORITY'],
                status = interface_result[i]['status'],
                resolution = interface_result[i]['resolution'],
                CREATED = interface_result[i]['CREATED'],
                UPDATED = interface_result[i]['UPDATED'],
            )
            interface.save()

        for i in range(len(nocasebug1_result)):
            nocasebug_result.append(nocasebug1_result[i])
        for i in range(len(nocasebug2_result)):
            nocasebug_result.append(nocasebug2_result[i])
        for i in range(len(nocasebug3_result)):
            nocasebug_result.append(nocasebug3_result[i])

        for i in range(len(nocasebug_result)):
            no = NoCaseBugModel(
                projectName = nocasebug_result[i]['projectName'],
                issuekey = nocasebug_result[i]['issuekey'],
                SUMMARY = nocasebug_result[i]['SUMMARY'],
                REPORTER = nocasebug_result[i]['REPORTER'],
                ASSIGNEE = nocasebug_result[i]['ASSIGNEE'],
                PRIORITY = nocasebug_result[i]['PRIORITY'],
                status = nocasebug_result[i]['status'],
                resolution = nocasebug_result[i]['resolution'],
                CREATED = nocasebug_result[i]['CREATED'],
                UPDATED = nocasebug_result[i]['UPDATED'],
            )
            no.save()

        # ===================================================================


        for i in range(len(ass1_result)):
            ass_result.append(ass1_result[i])
        for i in range(len(ass2_result)):
            ass_result.append(ass2_result[i])
        for i in range(len(ass3_result)):
            ass_result.append(ass3_result[i])

        for i in range(len(rep1_result)):
            rep_result.append(rep1_result[i])
        for i in range(len(rep2_result)):
            rep_result.append(rep2_result[i])
        for i in range(len(rep3_result)):
            rep_result.append(rep3_result[i])

        # 落地本地数据库
        for i in range(len(result)):
            p = PersonModel(
                lower_display_name = result[i]['lower_display_name'],
                lower_user_name = result[i]['lower_user_name']
            )
            p.save()

        for i in range(len(ass_result)):
            ass = AssignModel(
                projectName = ass_result[i]['projectName'],
                issuekey = ass_result[i]['issuekey'],
                SUMMARY = ass_result[i]['SUMMARY'],
                REPORTER = ass_result[i]['REPORTER'],
                ASSIGNEE = ass_result[i]['ASSIGNEE'],
                PRIORITY = ass_result[i]['PRIORITY'],
                status = ass_result[i]['status'],
                resolution = ass_result[i]['resolution'],
                CREATED = ass_result[i]['CREATED'],
                UPDATED = ass_result[i]['UPDATED'],
            )
            ass.save()

        for i in range(len(rep_result)):
            rep = ReporterModel(
                projectName = rep_result[i]['projectName'],
                issuekey = rep_result[i]['issuekey'],
                SUMMARY = rep_result[i]['SUMMARY'],
                REPORTER = rep_result[i]['REPORTER'],
                ASSIGNEE = rep_result[i]['ASSIGNEE'],
                PRIORITY = rep_result[i]['PRIORITY'],
                status = rep_result[i]['status'],
                resolution = rep_result[i]['resolution'],
                CREATED = rep_result[i]['CREATED'],
                UPDATED = rep_result[i]['UPDATED'],
            )
            rep.save()

        return HttpResponse("同步完成!!")
    else:
        return HttpResponse('没有权限!')

