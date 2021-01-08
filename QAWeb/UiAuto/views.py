from django.shortcuts import render

# Create your views here.

def index(request):
    context={}
    context['hi'] = 'hello world!'
    return render(request,'UIAuto/UIAuto.html',context)