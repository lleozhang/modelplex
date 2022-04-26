from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
# 表单
def signup_form(request):
    return render(request, 'signup_form.html')
 
# 接收请求数据
def signup(request):  
    request.encoding='utf-8'
    ctx ={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
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