from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import check
# 表单

# 接收请求数据
def signin(request):  
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
    if request.method == 'POST':
        if  request.POST['username'] and request.POST['password']:
            user1=User.objects.filter(name=request.POST['username'])
            if user1.count() == 0:
                ctx['rlt'] = '查无此用户！'
            else :
                pasword=request.POST['password']
                for var in user1:
                    pasword2=var.password
                if pasword==pasword2 :
                    ctx['username']=request.POST['username']
                    rep = redirect("/modelplex/profile/"+request.POST['username'])
                    rep.set_cookie('logged','true')
                    rep.set_cookie('username',request.POST['username'])
                    rep.set_cookie('password',pasword2)
                    return rep
                else :
                    ctx['rlt'] = '密码错误！'
        else:
            ctx['rlt'] = '用户名或密码不能为空'
    else :
        if Ctx[0] == 1:
            rep = redirect("/modelplex/profile/"+request.COOKIES.get('username'))
            return rep
    return render(request, "signin_form.html", ctx)

def logout(request):  
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
    rep = redirect("/modelplex/signin")
    rep.set_cookie('logged','false')
    return rep