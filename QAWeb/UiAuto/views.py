from django.shortcuts import render

from . import models

# Create your views here.

def index(request):
    Sces = models.UIAutoScenario.objects.all()

    context={}
    context['hi'] = 'hello world!'
    context['Scenarios'] = Sces
    return render(request,'UIAuto/UIAuto.html',context)