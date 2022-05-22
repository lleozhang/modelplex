from django.shortcuts import render
from Mod.models import ModInfo
import os
from . import s3

def upload(request):
    ctx={}
    if not request.COOKIES.get('logged') or request.COOKIES.get('logged')!='true':
        return render(request,'upload_result.html',{'response':'请登录后再上传！'})
    else:
        ctx['username']=request.COOKIES.get('username')
    return render(request,'upload.html',ctx)



def result(request):
    name = request.POST['q1']
    description = request.POST['q2']
    name = name.strip()
    description = description.strip()
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
    response=""
    flag=0

    if name == "":
        response+="模型名称不能为空！  "
        flag=1

    if description == "":
        response+="模型描述不能为空！ "
        flag=1

    File= request.FILES.get('upload',None)
    if File is None:
        response+="请选择上传文件！  "
        flag=1

    if flag==0:
        for var in ModInfo.objects.all():
            if var.name==name:
                flag=1
                response="与别的模型重名了！"
                break

    if flag==0:
        mod = ModInfo(name=name, description=description, owner=request.COOKIES.get('username'),accuracy=0.75, add="",visible=0)
        mod.save()
        with open(str(mod.id) + '.h5', 'wb+') as f:
            for chunk in File.chunks():
                f.write(chunk)
    ctx['response']=response
    if flag==1:
        return render(request,'upload_result.html',ctx)
    else:
        return render(request,"model.html",ctx)
