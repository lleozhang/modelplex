import os

from django.http import HttpResponse
from django.shortcuts import render
from Mod.models import ModInfo
from User.models import User
from Datasetinfo.models import Dataset
from TestHistory.models import History
import json
from . import s3
from . import check

def faq(request):
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
    return render(request, 'faq.html', ctx)


def all_datasets(request):
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
    dataset = Dataset.objects.filter(visible=1)
    ctx['datasetlist'] = dataset
    return render(request, 'all_dataset.html', ctx)


def all_models(request):
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
    model = ModInfo.objects.filter(visible=1)
    ctx['modellist'] = model
    return render(request, 'all_model.html', ctx)


def homepage(request):
    ctx = {}
    Ctx = check.check_login(request, ctx)
    ctx = Ctx[1]
    if Ctx[0] == -1:
        response = '请不要胡乱修改我们的COOKIE，这样做很不好！！！'
        ctx['response'] = response
        rep=render(request, 'result.html', ctx)
        rep.set_cookie('logged','false')
        rep.set_cookie('username',None)
        rep.set_cookie('password',None)
        return rep
    modellist=ModInfo.objects.filter(visible=1)
    ctx['modellist']=modellist
    ctx['datasetlist']=Dataset.objects.filter(visible=1)
    return render(request, 'mainpage.html', ctx)

def test_result(request,id):
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
    var = History.objects.get(id=id)
    ctx['history']=var
    return render(request,'testhistory.html',ctx)

def show_model(request):
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
    if request.method == 'GET':
        name = request.GET['name']
        var = ModInfo.objects.get(name=name)
        if var.visible == 0:
            var.delete()
            response = "该模型上传时遇到了错误，现不能正常访问，请您稍后再试或查看其他模型！"
            ctx['response'] = response
            return render(request, "result.html", ctx)
        modify_add = "/modelplex/model/" + str(var.id) + "/modify_model"
        del_add = "/modelplex/model/" + str(var.id) + "/delete_result"
        test_add = "/modelplex/model/" + str(var.id) + "/test_model"

        response_owner = "<a href='/modelplex/profile/"
        # if not request.COOKIES.get('logged') or request.COOKIES.get('logged') != 'true' or request.COOKIES.get(
        #        'username') != var.owner:
        response_owner += var.owner + '/'
        response_owner += "'>" + var.owner + "</a>"
        historylist=History.objects.filter(model_id=var.id)
        ctx.update({'response_id': var.id,
                    'response_name': var.name,
                    'response_description': var.description,
                    'response_add': var.add,
                    "modify_add": modify_add,
                    'del_add': del_add,
                    'test_add': test_add,
                    'historylist':historylist,
                    'response_owner': response_owner})
        rep = render(request, "model.html", ctx)
        return rep

    else:
        name = request.POST['q1']
        description = request.POST['q2']
        name = name.strip()
        description = description.strip()
        label = request.POST['label']

        response = ""
        flag = 0

        if name == "" or name is None:
            response += "模型名称不能为空！  "
            flag = 1

        if description == "" or description is None:
            response += "模型描述不能为空！ "
            flag = 1

        if flag == 0:
            for var in ModInfo.objects.all():
                if var.name == name:
                    flag = 1
                    response = "与别的模型重名了！"
                    break
        if label == 'keras':
            File = request.FILES.get('upload', None)
            if File is None:
                response += "请选择上传文件！  "
                flag = 1

            if File is not None:
                nm = File.name
                nm = nm.split('.')[-1]
                if nm != 'h5':
                    response += '不支持的文件类型！ '
                    flag = 1

            if flag == 1:
                ctx['response'] = response
                return render(request, "upload_result.html", ctx)

            else:
                mod = ModInfo(name=name, description=description, accuracy=0.75, tests=0,
                              owner=request.COOKIES.get('username'), add="", homepage="/modelplex/model/?name=" + name,
                              visible=0, type=0)
                mod.save()
                with open('static/file/' + str(mod.id) + '.h5', 'wb+') as f:
                    for chunk in File.chunks():
                        f.write(chunk)
                mod.visible = 1
                mod.save()

                modify_add = "/modelplex/model/" + str(mod.id) + "/modify_model"
                del_add = "/modelplex/model/" + str(mod.id) + "/delete_result"
                test_add = "/modelplex/model/" + str(mod.id) + "/test_model"
                response_owner = "<a href = '/modelplex/profile/"
                response_owner += mod.owner + '/'
                response_owner += "'>" + mod.owner + "</a>"
                historylist = History.objects.filter(model_id=var.id)
                ctx.update({'response_id': mod.id, 'response_name': mod.name, 'response_description': mod.description,
                            'response_add': mod.add, "modify_add": modify_add, 'del_add': del_add,
                            'test_add': test_add, 'response_owner': response_owner,'historylist':historylist})

                rep = render(request, "model.html", ctx)
                return rep
        else:
            File1 = request.FILES.get('upload1', None)

            File3 = request.FILES.get('upload3', None)
            if File1 is None or File3 is None:
                response += '请选择上传文件！'
                flag = 1
            if File1 is not None:
                nm = File1.name
                nm = nm.split('.')[-1]
                if nm != 'py':
                    response += '模型结构文件必须是.py文件！ '
                    flag = 1

            if File3 is not None:
                nm = File3.name
                nm1 = nm.split('.')[-1]
                nm2 = nm.split('.')[-2]
                if nm1 != 'tar' or nm2 != 'pth':
                    response += '模型参数文件必须是.pth.tar文件！ '
                    flag = 1
            if flag == 1:
                ctx['response'] = response
                return render(request, "upload_result.html", ctx)

            else:
                mod = ModInfo(name=name, description=description, accuracy=0.75, tests=0,
                              owner=request.COOKIES.get('username'), add="", homepage="/modelplex/model/?name=" + name,
                              visible=0, type=1)
                mod.save()
                with open('static/file/' + str(mod.id) + '.py', 'wb+') as f:
                    for chunk in File1.chunks():
                        f.write(chunk)


                with open('static/file/' + str(mod.id) + '.pth.tar', 'wb+') as f:
                    for chunk in File3.chunks():
                        f.write(chunk)

                mod.visible = 1
                mod.save()

                modify_add = "/modelplex/model/" + str(mod.id) + "/modify_model"
                del_add = "/modelplex/model/" + str(mod.id) + "/delete_result"
                test_add = "/modelplex/model/" + str(mod.id) + "/test_model"
                response_owner = "<a href = '/modelplex/profile/"
                # if not request.COOKIES.get('logged') or request.COOKIES.get('logged')!='true' or request.COOKIES.get('username')!=mod.owner:
                response_owner += mod.owner + '/'
                response_owner += "'>" + mod.owner + "</a>"
                historylist = History.objects.filter(model_id=var.id)
                ctx.update({'response_id': mod.id, 'response_name': mod.name, 'response_description': mod.description,
                            'response_add': mod.add, "modify_add": modify_add, 'del_add': del_add, 'test_add': test_add,
                            'response_owner': response_owner,'historylist':historylist})

                rep = render(request, "model.html", ctx)
                return rep
