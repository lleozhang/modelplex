import os
from django.shortcuts import render
from Mod.models import ModInfo
from Datasetinfo.models import Dataset
from django.http import HttpResponse
from . import s3,run_model
import json

import random
import string


def random_string(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


def test_model(request,id):
    ctx={}
    if not request.COOKIES.get('logged') or request.COOKIES.get('logged')!='true':
        return render(request,'test_result.html',{'response':'请登录后再测试模型！'})
    ctx['username']=request.COOKIES.get('username')

    address = "<a href = '/modelplex/model/" + str(id) + "/dataset_upload'> 或上传本地数据集 </a>"
    result = "/modelplex/model/" + str(id) + "/test_model/test_result"

    ctx.update({'address':address,'result':result})
    return render(request,'test_model.html',ctx)

def result(request,id):
    ctx = {}
    if request.COOKIES.get('logged') and request.COOKIES.get('logged')== 'true':
        ctx['username'] = request.COOKIES.get('username')
    chars = string.ascii_letters
    size = 15
    mod= ModInfo.objects.get(id=id)
    flag=0
    for dt in Dataset.objects.all():
        if dt.name==request.GET['q1']:
            flag=1
            break
    if flag==0:
        response="未找到该数据集，请返回测试页面手动上传！"
        rep = render(request, 'test_result.html', {"response": response})
        return rep

    dt = Dataset.objects.get(name=request.GET['q1'])

    str1 = random_string(size, chars)
    str2 = random_string(size, chars)
    str3 = random_string(size, chars)

    t1=s3.download_data('static/file/' + mod.name + str1 + '.h5', mod.name + '.h5', 'model')
    t2=s3.download_data('static/file/' + str(dt.id) + str2 + 'x.npy', str(dt.id) + 'x.npy', 'dataset')
    t3=s3.download_data('static/file/' + str(dt.id) + str3 + 'y.npy', str(dt.id) + 'y.npy', 'dataset')

    if t1==-1 or t2==-1 or t3==-1:
        response='由于某种原因，测试失败，请重新尝试！'
        ctx['response'] = response
        rep = render(request, 'test_result.html', ctx)
        return rep

    size, accu = run_model.test_model('static/file/' + mod.name + str1 + '.h5',
                                      'static/file/' + str(dt.id) + str2 + 'x.npy',
                                      'static/file/' + str(dt.id) + str3 + 'y.npy')

    os.remove('static/file/' + mod.name + str1 + '.h5')
    os.remove('static/file/' + str(dt.id) + str2 + 'x.npy')
    os.remove('static/file/' + str(dt.id) + str3 + 'y.npy')

    if size==-1 and accu==-1:
        response = '模型测试失败，您提交的数据集无法正常在该模型上运行，请检查你提交的数据集大小是否正确、测试数据与标签是否匹配、数据集格式与模型描述中要求是否一致！'
        ctx['response']=response
        rep = render(request, 'test_result.html', ctx)
        return rep

    cor=accu*size
    orc=mod.tests*mod.accuracy
    mod.tests+=size
    mod.accuracy=((orc+cor)/mod.tests)
    mod.save()
    response="模型测试成功，此次测试了"+str(size)+'组数据，准确率为'+str(accu)
    ctx['response']=response
    rep = render(request,'test_result.html',ctx)
    return rep
