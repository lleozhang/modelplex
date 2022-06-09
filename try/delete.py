from django.shortcuts import render
from Mod.models import ModInfo
from django.http import HttpResponse
from . import s3,check
import json
import os


def result(request,id):
    response=""
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
        var=ModInfo.objects.filter(id=id)
        if len(var)==0:
            ctx['response']='该模型已被别人删除，你来晚了...'
        else:
            var=var[0]
            if var.owner != request.COOKIES.get('username'):
                ctx['response']='你不能删除别人的模型！'
            else:
                if var.type==0:
                    os.remove('static/file/'+str(var.id)+'.h5')
                    var.delete()
                    ctx['response']="删除模型成功！"
                    rep = render(request,"delete_result.html",ctx)
                    return rep
                else:
                    os.remove('static/file/' + str(var.id) + '.py')
                    os.remove('static/file/' + str(var.id) + '.pth.tar')
                    var.delete()
                    ctx['response'] = "删除模型成功！"
                    rep = render(request, "delete_result.html", ctx)
                    return rep
    else:
        ctx["response"]='请登录后尝试删除！'
    return render(request, 'delete_result.html', ctx)
