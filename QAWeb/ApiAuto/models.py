from django.db import models

# Create your models here.

class ApiAutoScenario(models.Model):
    '''
     API automation test scenarios.
    '''
    scenarioId = models.IntegerField(unique=True)
    desc=models.CharField('Scenarios description',max_length=120)
    steps = models.TextField('Scenario steps')
    isAutomated = models.BooleanField(default=False)
    createDate=models.DateTimeField(auto_now_add=True)
    lastUdpateDate=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.desc
    
    
    class Meta:
        db_table='ApiAutoScenario'
        ordering=['scenarioId']

class ApiAutoCode(models.Model):
    '''
     API automation test code.
    '''
    sautoId = models.ForeignKey(ApiAutoScenario,to_field='scenarioId',on_delete=models.CASCADE,default=1)
    author=models.CharField('automation code author',max_length=20)
    desc=models.CharField('automation code description',max_length=120)
    createDate=models.DateTimeField(auto_now_add=True)
    lastUdpateDate=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sautoId)

    class Meta:
        db_table='ApiAutoCode'
        ordering=['sautoId']        
