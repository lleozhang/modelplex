from . import testmodel 
from Mod.models import ModInfo
from Datasetinfo.models import Dataset

def result(request,mod_id,data_id):
    mod=ModInfo.objects.get(id=mod_id)
    dt=Dataset.objects.get(id=data_id)
    lst=0
    recall=-1
    loss=-1
    if mod.type==0:
        dataset_dir='static/file/'
        if dt.uselink==1:
            dataset_dir+=dt.name+'/'
        lst=testmodel.test_keras(
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
         lst=testmodel.test_pytorch( mod.id,
                                     'static/file/' + str(dt.id)  + '.tar.gz',
                                     'static/file/' + str(mod.id)  + '.pth.tar',
                                     True,
                                     1,
                                     None,
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