import os
from django.shortcuts import render
from Mod.models import ModInfo
from Datasetinfo.models import Dataset
from TestHistory.models import History
from django.http import HttpResponse
from . import s3,run_model
from . import testmodel 
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

# from pytorch_test.pytorch_test import testnet
import json

import random
import string

def test_model(request,id):
    ctx={}
    ctx['result_name'] ="测试结果"
    if not request.COOKIES.get('logged') or request.COOKIES.get('logged')!='true':
        response="请登录后再测试模型！"
        ctx['response'] = response
        return render(request,'result.html',ctx)
    ctx['username']=request.COOKIES.get('username')

    address = "<a href = '/modelplex/model/" + str(id) + "/dataset_upload'> 或上传本地数据集 </a>"
    result = "/modelplex/model/" + str(id) + "/test_model/test_result"

    ctx.update({'address':address,'result':result})
    ctx['datasetlist']=Dataset.objects.all()
    ctx['testing']="/modelplex/model/" + str(id) + "/testing"

    mod= ModInfo.objects.get(id=id)
    ctx['model_type']=mod.type
    
    return render(request,'test_model.html',ctx)

def testing(request,id):
    ctx={}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')== 'true':
        ctx['username'] = request.COOKIES.get('username')
    ctx['size']=testmodel.siz
    ctx['response']=testmodel.cnt
    return render(request,'testing.html',ctx)

def result(request,id):
    ctx = {}
    ctx['result_name'] ="测试结果"
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')== 'true':
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
        lst=testmodel.test_keras(
            'static/file/' + str(dt.id)  + 'x.npy',
            'static/file/' + str(dt.id)  + 'y.npy',
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
         lst=testmodel.test_pytorch(
                                     'static/file/' + str(dt.id)  + '.tar.gz',
                                     'static/file/' + str(mod.id)  + '.pth.tar',
                                     'pytorch_test/etc/cifar10_bn.json',
                                     True,
                                     1
                                    )
         if lst!=-1:
             size,accu,loss,recall=lst
    
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
