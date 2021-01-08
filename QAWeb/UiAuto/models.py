from django.db import models

# Create your models here.

class UIAutoScenario(models.Model):
    '''
     Web UI automation test scenarios.
    '''
    scenarioId = models.IntegerField(unique=True)
    desc=models.CharField('Scenarios description',max_length=120)
    steps = models.TextField('Scenario steps')
    createDate=models.DateTimeField(auto_now_add=True)
    lastUdpateDate=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='UIAutoScenario'
        ordering=['scenarioId']

class UIAutoCode(models.Model):
    '''
     Web UI automation test code.
    '''
    sautoId = models.ForeignKey(UIAutoScenario,to_field='scenarioId',on_delete=models.CASCADE,default=1)
    author=models.CharField('automation code author',max_length=20)
    desc=models.CharField('automation code description',max_length=120)
    createDate=models.DateTimeField(auto_now_add=True)
    lastUdpateDate=models.DateTimeField(auto_now=True)

    class Meta:
        db_table='UIAutoCode'
        ordering=['sautoId']        
