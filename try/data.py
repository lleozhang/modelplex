import os
from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render
from User.models import User
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import s3
# 表单
from Datasetinfo.models import Dataset


def runoob(request):
    hello = "Hello World"
    return render(request, 'runoob.html', {"hello": hello})


def dataset(request, nowid):
    request.encoding = 'utf-8'
    ctx = {}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true':
        ctx['username'] = request.COOKIES.get('username')
    dataset1 = Dataset.objects.filter(id=nowid)
    ccnt = 0
    if dataset1.count() > 0:
        for var in dataset1:
            ctx['data_name'] = var.name
            ctx['data_description'] = var.description
            ctx['accuracy'] = var.accur
        return render(request, "dataset_info.html", ctx)
    return HTTPResponse("error")


def dataset_upload(request, mid):
    request.encoding = 'utf-8'
    ctx = {}
    result = "/modelplex/model/" + str(mid) + "/dataset_upload/"
    ctx['result'] = result
    if request.COOKIES.get('logged') and request.COOKIES.get('logged') == 'true':
        ctx['username'] = request.COOKIES.get('username')
        if request.method == 'POST':
            if request.FILES and request.POST.get('dataname') and request.POST.get('datadescription'):
                filex = request.FILES.get("dataset")
                filey = request.FILES.get('verifydataset')
                nm = request.POST.get('dataname')
                dc = request.POST.get('datadescription')

                flag=0
                for var in Dataset.objects.all():
                    if nm==var.name:
                        ctx['rlt'] = "与别的数据集重名了！"
                        flag=1
                if flag==1:
                    return render(request, "dataset_upload.html", ctx)
                # s3


                dataset1 = Dataset(name=nm, description=dc, owner=request.COOKIES.get('username'), modelid=mid,
                                   accur=1,visible=0)
                dataset1.save()

                with open('static/file/' + str(dataset1.id) + 'x.npy', 'wb') as f:
                    f.write(filex.read())

                with open('static/file/' + str(dataset1.id) + 'y.npy', 'wb') as f:
                    f.write(filey.read())

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
