# -*- coding:utf-8 -*-
import time

from MainReport import config
from MainReport.MySQLUtil import Connection

__author__ = 'kiven'

'''工具类'''
class myUtil(object):

    def __init__(self):
        pass

    # 获取sql语句
    def getSQLStatement(self,sqlfile):
        _SQLFILE = open(sqlfile)
        _SQL = _SQLFILE.read()
        _SQLFILE.close()
        return _SQL

    # 获取sql执行结果
    def getQueryResult(self,sql):
        conn = Connection(config._HOST, database=config._DB, user=config._USER, password=config._PASS, port=config._PORT)
        result = conn.query(sql)
        conn.close()
        return result

    # 当天日期
    @property
    def nowTime(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))


    # 获取指定数据(封装getProName()和getPerson()方法)
    def getDataList(self,queryResult,field,t = None):

        '''字段名称(项目名、组内各成员名等)
        '''
        dataList = []

        '''初始化该字段的状态 一般status = {'open':0,'inp rogress':0,'resolved':0,'closed':0}
        '''

        # 获取所有field字段放入dataList中,并初始化allInfo字典
        for row in range(len(queryResult)):
            f = queryResult[row][field]
            if f == '':
                f = u'未规划'
            if not f in dataList:
                dataList.append(f)
        return dataList

    # 获取指定数据的状态
    def getDataStatus(self,queryResult,field,status,myfield):
        dataStatus = status
        for row in range(len(queryResult)):
            s = queryResult[row]['status']
            f = queryResult[row][field]
            if f == myfield:
                dataStatus[s] += 1
        return dataStatus


    # 获取所有不重复项目名称
    '''
    废弃
    '''
    def getProName(self,queryResult):
        projectName = []
        # row即为一条issue
        for row in range(len(queryResult)):
            if queryResult[row]['projectName'] == "":
                queryResult[row]['projectName'] = u'未规划项目'
            if not queryResult[row]['projectName'] in projectName:
                projectName.append(queryResult[row]['projectName'])
        return projectName

    # 获取指定项目下指定状态的BUG的数量
    def getProStatus(self,queryResult,projectName):
        # 各状态数量
        projectStatus = {
            'Open':0,
            'Closed':0,
            'Resolved':0,
            'InProgress':0,
            'todayOpen':0,
            'todayReopen':0,
            'todayClose':0,
            "total":0
        }

        '''
        open、closed、resolved、reopen in today、closed in today
        '''
        for row in range(len(queryResult)):
            today = self.nowTime
            if queryResult[row]['projectName'] == projectName:
                if queryResult[row]['status'] == 'Open':
                    projectStatus['Open'] += 1
                    projectStatus['total'] += 1
                elif queryResult[row]['status'] == 'In Progress':
                    projectStatus['InProgress'] += 1
                    projectStatus['total'] += 1
                elif queryResult[row]['status'] == 'Closed':
                    projectStatus['Closed'] += 1
                    projectStatus['total'] += 1
                elif queryResult[row]['status'] == 'Resolved':
                    projectStatus['Resolved'] += 1
                    projectStatus['total'] += 1
                if str(queryResult[row]['CREATED']).split(' ')[0] == today:
                    projectStatus['todayOpen'] += 1
                if queryResult[row]['status'] == 'Reopened' and str(queryResult[row]['UPDATED']).split(' ')[0] == today:
                    projectStatus['todayReopen'] += 1
                if queryResult[row]['status'] == 'Closed' and str(queryResult[row]['UPDATED']).split(' ')[0] == today:
                    projectStatus['todayClose'] += 1

        return projectStatus

    # 获取成员
    '''
    废弃
    '''
    def getPerson(self,queryResult):
        personalInfo = []
        for row in range(len(queryResult)):
            if not queryResult[row]['REPORTER'] in personalInfo:
                personalInfo.append(queryResult[row]['REPORTER'])
        return personalInfo

    # 获取指定成员各个状态的BUG
    def getBugStatus(self,queryResult,personName):
        bugStatus = {
            'closed':0,
            'open':0,
            'resolved':0,
            'inprogess':0,
            'total':0
        }

        for row in range(len(queryResult)):
            if queryResult[row]['REPORTER'] in personName:
                if queryResult[row]['status'] == 'Closed':
                    bugStatus['closed'] += 1
                    bugStatus['total'] += 1
                elif queryResult[row]['status'] == 'Open':
                    bugStatus['open'] += 1
                    bugStatus['total'] += 1
                elif queryResult[row]['status'] == 'Resolved':
                    bugStatus['resolved'] += 1
                    bugStatus['total'] += 1
                elif queryResult[row]['status'] == 'In progress':
                    bugStatus['inprogess'] += 1
                    bugStatus['total'] += 1

        return bugStatus





#
# #
# u = myUtil()
# sql = u.getSQLStatement('../static/SQL/getPerson.sql')
# result = u.getQueryResult(sql)
# # # print str(result[0]['CREATED']).split(' ')[0]
# # # # print time.strptime('yyyy-mm-dd',result[0]['CREATED'])
# # # print u.timeFormat()
# # print u.getPersonalInfo(result)
# sta = {
#     'Open':0,
#     'In progress':0,
#     'Resolved':0,
#     'Closed':0,
# }
# print u.getAllInfo(result,'REPORTER',sta)


