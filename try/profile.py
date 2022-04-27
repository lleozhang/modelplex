from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from Mod.models import ModInfo
# 表单
from Datasetinfo.models import Dataset
# 接收请求数据
def profile(request,name):  
    request.encoding='utf-8'
    ctx ={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') =='true':
        ctx['username']=name
        dataset1=Dataset.objects.filter(owner=name,visible=1)
        models=ModInfo.objects.filter(owner=name,visible=1)
        ctx['datasetlist']=dataset1
        ctx['modellist']=models
        if name == request.COOKIES.get('username'):
            return render(request, "profile.html",ctx)
        else :
            return render(request, "others_profile.html",ctx)
    else:
        return HttpResponseRedirect('/modelplex/signin')

def mp_view(request):
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') =='true':
        ctx['username']=request.COOKIES.get('username')
    return render(request,"modify_password.html",ctx)

def modify_password(request):
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') =='true':
        last=request.POST["last_password"]
        now=request.POST["now_password"]
        renow=request.POST["repeat_password"]
        user1=User.objects.filter(name=request.COOKIES.get('username'))
        ctx={}
        ctx['result_name']="修改结果"
        ctx['username']=request.COOKIES.get('username')
        for var in user1:
            if var.password != last:
                ctx['response']="原密码错误"
                return render(request,"result.html",ctx)
            else :
                if now != renow :
                    ctx['response']="两次密码不一致"
                    return render(request,"result.html",ctx)
                var.password=now
                var.save()
                ctx['response']="修改成功！"
        return render(request,"result.html",ctx)