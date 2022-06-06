import os
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import s3,check
# 表单
from Datasetinfo.models import Dataset
from Mod.models import ModInfo

def runoob(request):
    hello = "Hello World"
    return render(request, 'runoob.html', {"hello": hello})


def dataset(request, nowid):
    request.encoding = 'utf-8'
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
    dataset1 = Dataset.objects.filter(id=nowid)
    ccnt = 0
    if dataset1.count() > 0:
        for var in dataset1:
            ctx['data_name'] = var.name
            ctx['data_description'] = var.description
            ctx['data_link']=var.link
        return render(request, "dataset_info.html", ctx)
    return HTTPResponse("error")


def dataset_upload(request, mid):
    request.encoding = 'utf-8'
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
    result = "/modelplex/model/" + str(mid) + "/dataset_upload/"
    ctx['result'] = result
    modset=ModInfo.objects.filter(id=mid)
    mymod=0
    for var in modset:
        ctx['model_type']=var.type
        mymod=var
    if Ctx[0] == 1:
        if request.method == 'POST':
            if request.POST.get('dataname') and request.POST.get('datadescription'):
                filex=0
                filey=0
                nm = request.POST.get('dataname')
                dc = request.POST.get('datadescription')
                lk = ''
                lb = request.POST.get('label')
                uselink=1
                if lb=='file':
                    uselink=0
                    lk='无'
                    if request.FILES==0:
                        ctx['rlt'] = "文件不能为空"
                        return render(request, "dataset_upload.html", ctx)
                    filex = request.FILES.get("dataset")
                    if mymod.type==0:
                        filey = request.FILES.get('verifydataset')
                        if filey==0:
                            ctx['rlt'] = "文件不能为空"
                            return render(request, "dataset_upload.html", ctx)
                else:
                    lk = request.POST.get('datalink')
                    if lk=='':
                        ctx['rlt'] = "链接不能为空"
                        return render(request, "dataset_upload.html", ctx)
                flag=0
                for var in Dataset.objects.all():
                    if nm==var.name:
                        ctx['rlt'] = "与别的数据集重名了！"
                        flag=1
                if flag==1:
                    return render(request, "dataset_upload.html", ctx)
                # s3


                dataset1 = Dataset(name=nm, description=dc, owner=request.COOKIES.get('username'), modelid=mid,link=lk,
                                   accur=1,visible=0,uselink=uselink)
                dataset1.save()
                if uselink==1:
                    dataset1.visible=1
                    dataset1.save()
                    rep = redirect("/modelplex/dataset/" + str(dataset1.id))
                    return rep
                if mymod.type==0:
                    with open('static/file/' + str(dataset1.id) + 'x.npy', 'wb') as f:
                        f.write(filex.read())

                    with open('static/file/' + str(dataset1.id) + 'y.npy', 'wb') as f:
                        f.write(filey.read())
                else:
                    with open('static/file/' + str(dataset1.id) + '.tar.gz', 'wb') as f:
                        f.write(filex.read())
                dataset1.visible=1
                dataset1.save()
                rep = redirect("/modelplex/dataset/" + str(dataset1.id))
                return rep
            else:
                ctx['rlt'] = "文件、名字和描述均不能为空"

    else:
        rep = redirect("/modelplex/signin")
        return rep
    return render(request, "dataset_upload.html", ctx)
