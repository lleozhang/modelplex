from keras import models
import os
import math
import numpy as np
import random
import importlib
from attrdict import AttrDict

import torch
#torch.cuda.current_device()
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader
import torch.utils
import utils
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from keras.utils import np_utils
import sys
#if '/root/modelplex/try/model' not in sys.path:
 #   sys.path.append("/root/modelplex/try/nets") 
#from models import HYPERWRN

try:
    if '/root/modelplex/try/model/' not in sys.path:
        sys.path.append("/root/modelplex/try/model/") 
    from models import MODEL,load_data
except Exception as e:
    with open("result.txt","w")as f:
       f.write('-1')
    os.remove('/root/modelplex/try/model/models.py')
import tarfile

from torch import utils
import json
import dill

import logging

import traceback

#help(models)
global cnt
cnt=0
global siz
siz=10000
class CIFAR10():
    MEAN = (0.485, 0.456, 0.406)
    STD = (0.229, 0.224, 0.225)
    NUM_CLASSES = 10
    IMAGE_SIZE = [32, 32]
    IMAGE_CHANNELS = 3

    def __init__(self):
        transform = transforms.Compose([transforms.ToTensor(),
                                        transforms.Normalize(self.MEAN, self.STD)])
        self.load_dataset(transform)
    def load_dataset(self, transform):
        self.trainset = torchvision.datasets.CIFAR10(root="./data", transform=transform, download=False)
        self.testset = torchvision.datasets.CIFAR10(root="./data", train=False, transform=transform, download=False)



def test_pytorch(model_id,data_path,model_path,config_path = None,need_loss = True,need_recall = 1):
    try:
        # 限制了CPU核数
        torch.set_num_threads(1)
        net = MODEL()
        
        checkpoint = torch.load(model_path)
        net = checkpoint
        net.eval()
        print("model been loaded")
        # print(net)
        if config_path != None:
            with open(config_path) as config_json_file:
                config = json.load(config_json_file)
            num_vs = config['num_specialists']
        print('here!')
        testLoader = load_data(data_path)
        print("data been loaded")
        os.remove('/root/modelplex/try/model/models.py')
        criterion = nn.CrossEntropyLoss()
        net = net.to("cpu")
        correct = 0  # 预测正确的图片数
        total = 0  # 总共的图片数
        sum = 0
        loss = 0
        P = 0
        TP = 0
        # 由于测试的时候不需要求导，可以暂时关闭autograd，提高速度，节约内存
        print(233)
        with torch.no_grad():
            for data in testLoader:
                if sum % 100 == 0:
                    print(sum)
                '''
                if sum == 500:
                    break
                '''
                sum += 1
                global cnt
                cnt += 1
                images, labels = data
                images = images.to("cpu")
                labels = labels.to("cpu")
                outputs = net(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum()
                loss += criterion(outputs, labels).mean()
                if need_recall != None:
                    P += (labels == need_recall).sum()
                    for i in range(len(labels)):
                        if predicted[i] == labels[i] and labels[i] == need_recall:
                            TP += 1
        loss /= len(testLoader)
        print('10000张测试集中的准确率为: %d %%' % (100 * correct / total))
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        print(e)
        return [-1]    
    res = []
    res.append(len(testLoader)*4)
    res.append((correct / total).item())
    if need_loss != None:
        res.append((loss.item()))
    else:
        res.append(None)
    if need_recall != None:
        if P == 0:
            res.append(-1)
        else:
            res.append((TP/P).item())
    else:
        res.append(None)
    return res


if __name__ == '__main__':

    res2 = test_pytorch(sys.argv[1],sys.argv[2],sys.argv[3])
    print(res2)
    with open("result.txt","w")as f:
        for res in res2:
            f.write(str(res)+"\n")
    #res2 = test_pytorch("./data/cifar-10-python.tar.gz",'./model/final_cifar10_bn343.pth.tar',True,1,'./etc/cifar10_bn.json')
    #print(res2)