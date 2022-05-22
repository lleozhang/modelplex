from django.shortcuts import render
from Mod.models import ModInfo
from Datasetinfo.models import Dataset
def search(request):
    ctx = {}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true':
        ctx['username'] = request.COOKIES.get('username')
    return render(request,'search.html',ctx)

def result(request):
    name=request.GET['q']
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
    response=""
    flag=0
    for var in ModInfo.objects.all():
        if name in var.name and var.visible==1:
          flag=1
          response+=var.name+":"+"<a href='/modelplex/model/?name="+var.name+"'>直达模型</a>"+"\r\n\r\n"

    if flag==0:
        response="找不到这个模型，您要上传一个吗？" + " " + "<a href='/modelplex/upload_model'>上传模型</a>"
    ctx["response"]=response
    return render(request,'search_result.html',ctx)

def dataset_result(request):
    name=request.GET['q']
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
    response=""
    flag=0
    for var in Dataset.objects.all():
        if name in var.name and var.visible==1:
          flag=1
          response+=var.name+":"+"<a href='/modelplex/dataset/"+str(var.id)+"'>直达数据集主页</a>"+"\r\n\r\n"

    if flag==0:
        response="找不到这个数据集"
    ctx["response"]=response
    return render(request,'search_result.html',ctx)
