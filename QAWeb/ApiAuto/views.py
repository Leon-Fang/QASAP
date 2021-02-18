from . import models
from django.shortcuts import render,HttpResponse
import requests
from UiAuto.views import webOpt
import json
import pandas as pd
import numpy as np
import math
from pyecharts.charts import Bar

# Create your views here.

def index(request):
    Sces = models.ApiAutoScenario.objects.all()
    context = {}
    context['Scenarios'] = Sces
    return render(request,'ApiAuto/ApiAuto.html',context)

def runApiAutoTest(request):
    w =webOpt(r'statics/tools/chromedriver',30)
    acctoken=w.getAccToken('https://dmcazsysinthc1-dm-internal-azure-az-sysint-execution.cfapps.eu20.hana.ondemand.com','pe.tester1@sap.com','Sap1234567','dm-preprod.accounts400.ondemand.com','https://dmcazsysinthc1-dm-internal-azure-az-sysint-execution.cfapps.eu20.hana.ondemand.com/jwt')  
    a=apiAuto('https://dm-internal-azure-az-sysint-fnd-processengine.cfapps.eu20.hana.ondemand.com/api/v1/process/processDefinitions/start',acctoken)
    param= {'key':'REG_12c8292d-3943-48d5-b892-d156c32aac01_4','version':1,'async':'false','logLevel':'DEBUG'}
    b = '{"input1":[{      "lang":"zh",     "value":"vau",     "integerValue": 0,     "numValue": 10 },{      "lang":"zh",     "value":"vau",     "integerValue": 1,     "numValue": 10 } ],"input2":"[1,2,3,4.5]","passUserId":true}'
    res=a.runAPI(method="post",param=param,body=b)
    context = {}
    context['test'] = res.text
    return render(request,'ApiAuto/ApiAuto.html',context)

def runApiAutoTest2(request,sceId):
    context = {}
    w =webOpt(r'statics/tools/chromedriver',30)
    acctoken=w.getAccToken('https://dmcazsysinthc1-dm-internal-azure-az-sysint-execution.cfapps.eu20.hana.ondemand.com','pe.tester1@sap.com','Sap1234567','dm-preprod.accounts400.ondemand.com','https://dmcazsysinthc1-dm-internal-azure-az-sysint-execution.cfapps.eu20.hana.ondemand.com/jwt')   
    #1. input/expectResult/parameters/method
    inputs=models.ApiAutoCode.objects.filter(sautoId=sceId).get('ApiInput')
    expectResult=models.ApiAutoCode.objects.filter(sautoId=sceId).get('expectResult')
    params=models.ApiAutoCode.objects.filter(sautoId=sceId).get('ApiParam')
    method=models.ApiAutoCode.objects.filter(sautoId=sceId).get('ApiMethod')
    #2. allapi
    a=apiAuto('https://dm-internal-azure-az-sysint-fnd-processengine.cfapps.eu20.hana.ondemand.com/api/v1/process/processDefinitions/start',acctoken)
    res=a.runAPI(method=method,param=params,body=inputs)
    #4. verify result
    result=a.verifyResult(res,expectResult)
    context['test']=result
    return render(request,'ApiAuto/ApiAuto.html',context)

class apiAuto():
    def __init__(self,url,accToken):
        self.url = url
        self.accToken = accToken

    def runAPI(self, method, **kv):
        """
        run api to get data.
        """
        header = {}
        header['Authorization'] = "Bearer "+ self.accToken
        header['Content-Type']= "application/json"
        param = {}
        data = {}

        if "headers" in kv.keys():  
            header = dict(header, **kv['headers']) 
        if "param" in kv.keys():
            param = dict(param, **kv['param']) 
        if "body" in kv.keys():
            data = kv['body']
        
        if method == 'get':
            response = requests.get(self.url, headers=header, params=param)
        elif method == 'post':
            response = requests.post(self.url, headers=header, params=param, data=data)
        elif method == 'delete':
            response = requests.delete(self.url, headers=header, params=param)
        else:
            response = "method not implemented yet!"
        return response

    def verifyResult(self, response, **expectedResult):
        """
        docstring
        """
        apiResult=response.text
        outputs={}
        if "outputs" in expectedResult.keys():
            outputs=expectedResult['outputs']
            dict1 = json.load(apiResult)
            dict2 = json.load(outputs)
            #result=cmp(dict1,dict2)
        elif "statusCode" in expectedResult.keys():
            statusCode=expectedResult['statusCode']
            if statusCode==response.statusCode:
                result=0
        return result
         
    def __str__(self):
        "Process engine api automation test"


class analysisPerformanceResult(apiAuto):
    def __init__(self,url,token,insCSVFile,stepCSVFile):
        super.__init__(analysisPerformanceResult,self).__init__(url,token)
        '''
        get csv fiel via api
        '''
        df = pd.read_csv(insCSVFile)
        pi=df[df['InstanceName'].str.contains('run5SerialMockService',regex=False)]
        self.insDF=pi
        self.stepDF=pd.read_csv(stepCSVFile)
    
    def getTPS(self):
        """
        caculate tps.
        """
        df = self.insDF
        st = pd.to_datetime(df['StartTime'])
        et = pd.to_datetime(df['EndTime'])
        tps=df.shape[0]/(et.max()-st.min()).total_seconds()
        return tps
    
    def getResTime(self):
        """
        caculate response time.
        return like: 
        {
            'count': 100.0,
            'mean': 4759.06,
            'std': 854.870547468617,
            'min': 3981.0,
            '50%': 4482.5,
            '90%': 5765.0,
            '95%': 990029,
            '99%': 6703.510000000016,
            '99.9%': 9421.951000000032,
            'max': 9724.0
        }
        """
        df = self.insDF
        d=df['Duration'].sort_values().reset_index(drop = True)
        dic = dict(d.describe(percentiles=[.9,.95,.99,.999]))
        fifty=self.getPercentileValue(d,0.5)
        ninety=self.getPercentileValue(d,0.9)
        ninety5=self.getPercentileValue(d,0.95)
        ninety9=self.getPercentileValue(d,0.99)
        ninety99=self.getPercentileValue(d,0.999)
        dic['50%']=fifty
        dic['90%']=ninety
        dic['95%']=ninety5
        dic['99%']=ninety9
        dic['99.9%']=ninety99
        return dic
    
    def getPercentileValue(self,serieS,percentileV):
        '''
        return the value at the percentileV position.
        '''
        cnt=serieS.count()
        num=math.floor(cnt*percentileV)-1
        dvalue=serieS[num]
        return dvalue

    def getFailRate(self):
        '''
        return like: {'COMPLETED': 100, 'TERMINATED': 1, 'FAILED': 1} 
        '''
        df = self.insDF
        statusDic =dict(df['Status'].value_counts())
        return statusDic

    def getFailedInsName(self):
        '''
        return pd.series like: 100 sdferfddfdf
        '''
        df = self.insDF
        failInsName = df[df['Status'].str.contains('FAILED')]['InstanceName']
        return failInsName