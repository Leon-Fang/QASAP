from django.shortcuts import render
from selenium import webdriver
from . import models
import time
import json

# Create your views here.

def index(request):
    Sces = models.UIAutoScenario.objects.all()
    ats=getToken(request)
    context={}
    context['hi'] = 'hello world!'
    context['Scenarios'] = Sces
    context['ats'] = ats
    return render(request,'UIAuto/UIAuto.html',context)

def getToken(request):
    a =webOpt(r'statics/tools/chromedriver',30)
    # 'https://dmcsysint1-dm-internal-sysint-execution.cfapps.eu10.hana.ondemand.com '
    # 'pe.tester1@sap.com'
    # 'Sap1234567'
    # 'dm-preprod.accounts400.ondemand.com'
    # 'https://dmcsysint1-dm-internal-sysint-execution.cfapps.eu10.hana.ondemand.com/jwt'
    acctoken = a.getAccToken('https://dmcsysint1-dm-internal-sysint-execution.cfapps.eu10.hana.ondemand.com','pe.tester1@sap.com','Sap1234567','dm-preprod.accounts400.ondemand.com','https://dmcsysint1-dm-internal-sysint-execution.cfapps.eu10.hana.ondemand.com/jwt')  
    return acctoken

class webOpt:
    def __init__(self,chrome_path, EleWaittime):
        self.driver = webdriver.Chrome(executable_path=chrome_path)
        self.driver.implicitly_wait(EleWaittime)
        self.driver.maximize_window()

    def openUrl(self,url):
        """
        docstring
        """
        self.driver.get(url)
    
    def getAccToken(self, url, username, pwd, prelink,jwtUrl):
        """
        docstring
        """
        dr = self.driver
        dr.get(url)
        login_link = dr.find_element_by_link_text(prelink)
        login_link.click()
        time.sleep(3)

        dr.find_element_by_id('j_username').send_keys(username)
        dr.find_element_by_id('j_password').send_keys(pwd)
        dr.find_element_by_id("logOnFormSubmit").click()
        time.sleep(3)

        dr.get(jwtUrl)
        bodytext=dr.find_element_by_xpath("/html/body/pre")
        accToken = json.loads(bodytext.text).get('userInfo').get('token').get('accessToken')
        
        return accToken
