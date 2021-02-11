from . import models
from django.shortcuts import render,HttpResponse
import requests
from UiAuto.views import webOpt
import json

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
            result=cmp(dict1,dict2)
        elif "statusCode" in expectedResult.keys():
            statusCode=expectedResult['statusCode']
            if statusCode==response.statusCode:
                result=0
        return result
         
    def __str__(self):
        "Process engine api automation test"