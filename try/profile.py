from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from Mod.models import ModInfo
# 表单
from Datasetinfo.models import Dataset
from TestHistory.models import History
from . import check
# 接收请求数据
def profile(request,name):  
    request.encoding='utf-8'
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
    if Ctx[0] == 1:
        ctx['Username']=name
        ctx['username']=request.COOKIES.get('username')
        dataset1=[]
        models=[]
        for var in Dataset.objects.all():
            if var.owner==name and var.visible==1:
                dataset1.append(var)

        for var in ModInfo.objects.all():
            if var.owner==name and var.visible==1:
                models.append(var)

        ctx['datasetlist']=dataset1
        ctx['modellist']=models
        ctx['historylist']=History.objects.filter(hacker=name)
        is_my_profile=0
        if name == request.COOKIES.get('username'):
            is_my_profile=1
        ctx['is_my_profile']=is_my_profile
        return render(request, "profile.html",ctx)
    else:
        return HttpResponseRedirect('/modelplex/signin')

def mp_view(request):
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
    return render(request,"modify_password.html",ctx)

def modify_password(request):
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
    if Ctx[0] == 1:
        last=request.POST["last_password"]
        now=request.POST["now_password"]
        renow=request.POST["repeat_password"]
        user1=User.objects.filter(name=request.COOKIES.get('username'))
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
                rep = render(request, 'result.html', ctx)
                rep.set_cookie('password', now)
                return rep
        return render(request,"result.html",ctx)
