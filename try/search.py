from django.shortcuts import render
from Mod.models import ModInfo
def search(request):
    return render(request,'search.html')

def result(request):
    name=request.GET['q']
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
    response=""
    flag=0
    for var in ModInfo.objects.all():
        if name in var.name:
          flag=1
          response+=var.name+":"+"<a href='/modelplex/model/?name="+var.name+"'>直达模型</a>"+"\r\n\r\n"

    if flag==0:
        response="找不到这个模型，您要上传一个吗？" + " " + "<a href='/modelplex/upload_model'>上传模型</a>"
    ctx["response"]=response
    return render(request,'search_result.html',ctx)