from django.shortcuts import render
from Mod.models import ModInfo
from django.http import HttpResponse
from . import s3
import json
import os


def result(request,id):
    response=""
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')=='true':
        ctx['username']=request.COOKIES.get('username')
        var=ModInfo.objects.filter(id=id)
        if len(var)==0:
            ctx['response']='该模型已被别人删除，你来晚了...'
        else:
            var=var[0]
            if var.owner != request.COOKIES.get('username'):
                ctx['response']='你不能删除别人的模型！'
            else:
                os.remove('static/file/'+str(var.id)+'.h5')
                var.delete()
                ctx['response']="删除模型成功！"
                rep = render(request,"delete_result.html",ctx)
                return rep
    else:
        ctx["response"]='请登录后尝试删除！'
    return render(request, 'delete_result.html', ctx)
