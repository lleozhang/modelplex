import os
from django.shortcuts import render
from Mod.models import ModInfo
from Datasetinfo.models import Dataset
from TestHistory.models import History
from django.http import HttpResponse
from . import s3,run_model,test_keras
import time
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from . import check
# from pytorch_test.pytorch_test import testnet
import json

import random
import string

def test_model(request,id):
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
    ctx['result_name'] ="测试结果"
    if Ctx[0]==0:
        response="请登录后再测试模型！"
        ctx['response'] = response
        return render(request,'result.html',ctx)
    ctx['username']=request.COOKIES.get('username')

    address = "<a href = '/modelplex/model/" + str(id) + "/dataset_upload'> 或上传本地数据集 </a>"
    result = "/modelplex/model/" + str(id) + "/test_model/result/"

    ctx.update({'address':address,'result':result})
    ctx['datasetlist']=Dataset.objects.all()
    ctx['testing']="/modelplex/model/" + str(id) + "/testing"

    mod= ModInfo.objects.get(id=id)
    ctx['model_type']=mod.type
    
    return render(request,'test_model.html',ctx)

def testing(request,id):
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
    ctx['size']=testmodel.siz
    ctx['response']=testmodel.cnt
    return render(request,'testing.html',ctx)

def result(request,id):
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
    ctx['result_name'] ="测试结果"
    if Ctx[0]==0:
        ctx['username'] = request.COOKIES.get('username')
    mod= ModInfo.objects.get(id=id)
    if mod.visible==0:
        response="该模型目前不可用，请稍后尝试或换用其他模型！"
        ctx['response'] = response
        rep = render(request, 'result.html', ctx)
        return rep

    if 'q1' not in request.GET:
        response = "请选择一个数据集！"
        ctx['response'] = response
        rep = render(request, 'result.html', ctx)
        return rep

    dt = Dataset.objects.filter(name=request.GET['q1'])
    if len(dt)==0:
        response = "没有找到该数据集，请检查您输入的名称是否正确！"
        ctx['response'] = response
        rep = render(request, 'result.html', ctx)
        return rep

    dt=dt[0]
    if dt.visible==0:
        response = "该数据集目前不可用，请稍后尝试或换用其他数据集！"
        ctx['response'] = response
        rep = render(request, 'result.html', ctx)
        return rep
    
    

    lst=0
    recall=-1
    loss=-1
    if mod.type==0:
        dataset_dir='static/file/'
        if dt.uselink==1:
            dataset_dir+=dt.name+'/'
        lst=test_keras.test_keras(
            dataset_dir+ str(dt.id)  + 'x.npy',
            dataset_dir + str(dt.id)  + 'y.npy',
            'static/file/' + str(mod.id)  + '.h5',
            
            True,
            1
                                      
        )
        # size,accu,recall,loss= testmodel.test_keras(
        #                             'static/file/' + str(dt.id)  + 'x.npy',
        #                               'static/file/' + str(dt.id)  + 'y.npy',
        #                               'static/file/' + str(mod.id)  + '.h5',
        #                               )
        if lst!=-1:
             size,accu,loss,recall=lst
    
    else :
        #rep
        while os.path.exists('/root/modelplex/try/model/models.py'):
            time.sleep(1)
        with open('/root/modelplex/try/model/models.py','w') as f,open('/root/modelplex/static/file/'+str(mod.id)+'.py') as g:
            for w in g.readlines():
                f.write(w)
        print("to be test")
        cmd='python3 /root/modelplex/try/testmodel.py '+ str(mod.id)+' static/file/' + str(dt.id)  + '.tar.gz '+' static/file/' + str(mod.id)  + '.pth.tar '
        os.system(cmd)
        with open('result.txt','r') as f:
            lst=[float(w) for w in f.readlines()]
        os.remove('result.txt')
        if lst[0]!=-1:
            size,accu,loss,recall=lst
        else:
            cmd='python3 /root/modelplex/try/test_special.py '+ str(mod.id)+' static/file/' + str(dt.id)  + '.tar.gz '+' static/file/' + str(mod.id)  + '.pth.tar '
            os.system(cmd)
            with open('result.txt','r') as f:
                lst=[float(w) for w in f.readlines()]
            os.remove('result.txt')
            if lst[0]!=-1:
                size,accu,loss,recall=lst
            else:
                lst=-1
    
    if lst==-1 or (size==-1 and accu==-1):
        response = '模型测试失败，可能的原因是目前服务器容量已达到上限，您可以稍后再试；若您始终无法测试成功，可能的原因是您提交的数据集无法正常在该模型上运行，请检查您提交的数据集大小是否正确、测试数据与标签是否匹配、数据集格式与模型描述中要求是否一致！'
        ctx['response']=response
        rep = render(request, 'result.html', ctx)
        return rep
    result=History(
        hacker = ctx['username'],
        model_id = mod.id,
        dataset_id = dt.id,
        dataset_number = size,
        accuracy = accu,
        recall = recall,
        loss = loss
    )
    result.save()
    cor=accu*size
    orc=mod.tests*mod.accuracy
    mod.tests+=size
    mod.accuracy=((orc+cor)/mod.tests)
    mod.save()
    # response="模型测试成功，此次测试了"+str(size)+'组数据，准确率为'+str(accu)+'，召回率为'+str(recall)+'，损失函数为'+str(loss)
    # ctx['response']=response
    rep = redirect("/modelplex/testresult/"+str(result.id))
    return rep
    
