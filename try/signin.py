from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
# 表单

# 接收请求数据
def signin(request):  
    request.encoding='utf-8'
    ctx ={}
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
                    return rep
                else :
                    ctx['rlt'] = '密码错误！'
        else:
            ctx['rlt'] = '用户名或密码不能为空'
    else :
        if request.COOKIES.get('logged') and request.COOKIES.get('logged') =='true':
            rep = redirect("/modelplex/profile/"+request.COOKIES.get('username'))
            return rep
    return render(request, "signin_form.html", ctx)

def logout(request):  
    request.encoding='utf-8'
    ctx ={}
    rep = redirect("/modelplex/signin")
    rep.set_cookie('logged','false')
    return rep