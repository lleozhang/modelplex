from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from . import check
# 表单
def signup_form(request):
    return render(request, 'signup_form.html')
 
# 接收请求数据
def signup(request):  
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
    if request.POST and request.POST['username']:
        if request.POST['password']:
            pasword=request.POST['password']
            pasword2=request.POST['confirm_password']
            if pasword != pasword2:
                ctx['rlt'] = '两次输入密码不相同'
            else:
                user1=User.objects.filter(name=request.POST['username'])
                if user1.count() > 0:
                    ctx['rlt'] = '此用户已存在'
                else :
                    tmp=User(name=request.POST['username'],password=pasword)
                    tmp.save()
                    ctx['rlt'] = '注册成功！您的用户名为: ' + request.POST['username']
        else :
            ctx['rlt'] = '密码不能为空'
    else:
        ctx['rlt'] = '用户名不能为空'
    return render(request, "signup_form.html", ctx)