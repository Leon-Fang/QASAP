from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request,'Testing/TestHome.html',context)

def test11(reques):
    return HttpResponse("Hello test11")

def activity(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'Testing/Activities.html',context)
