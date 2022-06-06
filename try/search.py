from django.shortcuts import render
from Mod.models import ModInfo
from Datasetinfo.models import Dataset
from . import check
def search(request):
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
    return render(request,'search.html',ctx)

def result(request):
    name=request.GET['q']
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
    resultlist=[]
    for var in ModInfo.objects.all():
        if name in var.name and var.visible==1:
          resultlist.append(var)

    ctx["resultlist"]=resultlist
    return render(request,'search_result.html',ctx)

def dataset_result(request):
    name=request.GET['q']
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
    resultlist=[]

    for var in Dataset.objects.all():
        if name in var.name and var.visible==1:
          resultlist.append(var)

    ctx["resultlist"]=resultlist
    return render(request,'search_dataset_result.html',ctx)