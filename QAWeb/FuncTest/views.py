from django.shortcuts import render

def index(request):
    """
    For functional testing related contents.
    """
    context = {}
    context['hello'] = 'Hello func test'
    return render(request,'FuncTest/funcTest.html',context)

