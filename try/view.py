import os

from django.http import HttpResponse
from django.shortcuts import render
from Mod.models import ModInfo
from User.models import User
from Datasetinfo.models import Dataset
import json
from . import s3

def faq(request):
    ctx = {}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true':
        ctx['username'] = request.COOKIES.get('username')

    return render(request,'faq.html',ctx)

def all_datasets(request):
    ctx = {}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true':
        ctx['username'] = request.COOKIES.get('username')

    dataset = Dataset.objects.all()
    ctx['datasetlist'] = dataset
    return render(request, 'faq.html', ctx)

def homepage(request):
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true' :
        ctx['username']=request.COOKIES.get('username')
    return render(request,'mainpage.html',ctx)

def show_model(request):
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true' :
        ctx['username']=request.COOKIES.get('username')
    if request.method=='GET':
        name = request.GET['name']
        var=ModInfo.objects.get(name=name)
        if var.visible==0:
            var.delete()
            response="该模型上传时遇到了错误，现不能正常访问，请您稍后再试或查看其他模型！"
            ctx['response']=response
            return render(request, "result.html",ctx)
        modify_add = "/modelplex/model/" + str(var.id) + "/modify_model"
        del_add="/modelplex/model/" + str(var.id) + "/delete_result"
        test_add="/modelplex/model/" + str(var.id) + "/test_model"

        response_owner = "<a href='/modelplex/profile/"
        #if not request.COOKIES.get('logged') or request.COOKIES.get('logged') != 'true' or request.COOKIES.get(
        #        'username') != var.owner:
        response_owner += var.owner + '/'
        response_owner+="'>"+var.owner+"</a>"
        
        ctx.update({'response_id': var.id, 
        'response_name': var.name, 
        'response_description': var.description,
        'response_add':var.add,
        'response_accuracy':var.accuracy,
        'response_tests':var.tests,
        "modify_add":modify_add,
        'del_add':del_add,
        'test_add':test_add,
        'response_owner':response_owner})
        rep = render(request, "model.html",ctx)
        return rep

    else:
        name = request.POST['q1']
        description = request.POST['q2']
        name = name.strip()
        description = description.strip()

        response = ""
        flag = 0

        if name == "" or name is None:
            response += "模型名称不能为空！  "
            flag = 1

        if description == "" or description is None:
            response += "模型描述不能为空！ "
            flag = 1
        File = request.FILES.get('upload', None)
        if File is None:
            response += "请选择上传文件！  "
            flag = 1

        if flag == 0:
            for var in ModInfo.objects.all():
                if var.name == name:
                    flag = 1
                    response = "与别的模型重名了！"
                    break

        if flag==1:
            ctx['response']=response
            return render(request, "upload_result.html",ctx)

        if flag == 0:

            mod = ModInfo(name=name, description=description, accuracy=0.75, tests=0,owner=request.COOKIES.get('username'),add="",homepage="/modelplex/model/?name="+name,visible=0)
            mod.save()
            with open('static/file/'+str(mod.id) + '.h5', 'wb+') as f:
                for chunk in File.chunks():
                    f.write(chunk)
            mod.visible = 1
            mod.save()

            modify_add = "/modelplex/model/" + str(mod.id) + "/modify_model"
            del_add = "/modelplex/model/" + str(mod.id) + "/delete_result"
            test_add = "/modelplex/model/" + str(mod.id) + "/test_model"
            response_owner = "<a href = '/modelplex/profile/"
            #if not request.COOKIES.get('logged') or request.COOKIES.get('logged')!='true' or request.COOKIES.get('username')!=mod.owner:
            response_owner+=mod.owner+'/'
            response_owner += "'>"+mod.owner+"</a>"
            ctx.update({'response_id': mod.id, 'response_name': mod.name, 'response_description': mod.description,
                          'response_add': mod.add, 'response_accuracy': mod.accuracy,
                          'response_tests':mod.tests,"modify_add":modify_add,'del_add':del_add,'test_add':test_add,'response_owner':response_owner})
            
            rep = render(request, "model.html",ctx)
            return rep
