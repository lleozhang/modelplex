from django.shortcuts import render
from Mod.models import ModInfo
from django.http import HttpResponse
import json
from . import check

def modify(request,id):
    response=""
    ctx = {}
    Ctx = check.check_login(request, ctx)
    ctx = Ctx[1]
    if Ctx[0] == -1:
        response = '请不要胡乱修改我们的COOKIE，这样做很不好！！！'
        ctx['response'] = response
        return render(request, 'result.html', ctx)
    if Ctx[0] == 1:
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
    ctx = {}
    Ctx = check.check_login(request, ctx)
    ctx = Ctx[1]
    if Ctx[0] == -1:
        response = '请不要胡乱修改我们的COOKIE，这样做很不好！！！'
        ctx['response'] = response
        rep = render(request, 'result.html', ctx)
        rep.set_cookie('logged', 'false')
        rep.set_cookie('username', None)
        rep.set_cookie('password', None)
        return rep
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
