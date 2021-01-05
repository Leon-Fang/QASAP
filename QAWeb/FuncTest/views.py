from django.shortcuts import render,HttpResponse
from .models import CheckpointImage
from django.conf import settings

def index(request):
    """
    For functional testing related contents.
    """
    context = {}
    context['hello'] = 'Hello func test'
    return render(request,'FuncTest/funcTest.html',context)

def upload_action(request):
    """保存上传文件"""
    # 1.获取上传的文件
    pic = request.FILES['pic']
    # 2.创建文件
    save_path = '%s/checkpoint0/%s'%(settings.MEDIA_ROOT,pic.name)
    with open(save_path, 'wb') as f :
        # 获取上传文件的内容并写到创建文件中
        # pic.chunks():分块的返回文件
        for content in pic.chunks():
            f.write(content)
    # 3.将保存操作写到数据库中
    CheckpointImage.objects.create(testEv='checkpoint0/%s'%pic.name,description='first test')
    # 4.返回响应
    context = {}
    context['image1'] = save_path
    return render(request,'FuncTest/funcTest.html',context)
