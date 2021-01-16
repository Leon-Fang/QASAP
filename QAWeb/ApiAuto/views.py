from . import models
from django.shortcuts import render

# Create your views here.

def index(request):
    Sces = models.ApiAutoScenario.objects.all()

    context = {}

    context['Scenarios'] = Sces
    return render(request,'ApiAuto/ApiAuto.html',context)