from django.shortcuts import render
from Mod.models import ModInfo
from django.http import HttpResponse
import json


def modify(request,id):
    response=""
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
        var=ModInfo.objects.get(id=id)
        if request.COOKIES.get('username')!=var.owner:
            ctx["response"]='你不能修改别人的模型！'
        else:
            ctx["add"] = "/modelplex/model/" + str(id) + "/modify_model/modify_result"
            return render(request, 'modify.html', ctx)
    else:
        ctx["response"]='请登录后尝试修改！'
    return render(request,'modify_result.html',ctx)

def result(request,id):
    var=ModInfo.objects.get(id=id)
    name=var.name
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
    new_name=request.GET['q1']
    new_des=request.GET['q2']

    new_name=new_name.strip()
    new_des=new_des.strip()

    if new_name=="" and new_des!="":
        new_name=name
    elif new_des=="" and new_name!="":
        new_des=var.description
    elif new_name=="" and new_des=="":
        ctx["response"]="请至少输入点什么..."
        rep = render(request, "modify_result.html", ctx)
        return rep

    for v in ModInfo.objects.all():
        if v.name==new_name and v.name != name:
            ctx["response"]="与已有模型重名！"
            rep = render(request,"modify_result.html",ctx)
            return rep

    var.name=new_name
    var.description=new_des
    var.homepage='/modelplex/model/?name='+new_name
    var.save()
    ctx["response"]="修改模型成功！"
    rep = render(request,"modify_result.html",ctx)
    return rep
