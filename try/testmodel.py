from keras import models
import os
import math
import numpy as np
import random

from attrdict import AttrDict

import torch
#torch.cuda.current_device()
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import DataLoader

import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from keras.utils import np_utils

from .nets.models import HYPERWRN
import tarfile

from torch import utils
import json
import dill

import logging

import traceback
import sys
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




def test_keras(testx_path,testy_path,model_path,need_loss = 1,need_recall = 1):
    try:
        model = models.load_model(model_path)
        testx = np.load(testx_path)
        testy = np.load(testy_path)
        pred = model.predict(testx)
        recall = 0
        if (len(testx) != len(testy)):
            return -1
        # testx = testx.reshape((-1,784))
        if need_recall != None:
            P = 0
            TP = 0
            for i in range(len(testy)):
                if testy[i][need_recall] == 1:
                    P += 1
                    if np.argmax(pred[i]) == need_recall:
                        TP += 1
            recall = TP/P
        score = model.evaluate(testx, testy)
    except Exception as e:
        return -1
    res = []
    res.append(len(testx))
    res.append(score[1])
    if need_loss != None:
        res.append(score[0])
    else:
        res.append(-1)
    if need_recall != None:
        res.append(recall)
    else:
        res.append(-1)
    return res

def test_pytorch(data_path,model_path,config_path = None,need_loss = None,need_recall = None):
    print(0)
    print(sys.path)
    try:
        net = HYPERWRN()
        #限制了CPU核数
        torch.set_num_threads(1)
        checkpoint=torch.load(model_path,pickle_module = dill,map_location = torch.device('cpu'))
        net=checkpoint['model']
        net.eval()
        #print(net)
        if config_path!=None:
            with open(config_path) as config_json_file:
                config = json.load(config_json_file)
        num_vs = config['num_specialists']
        tf = tarfile.open(data_path)
        tf.extractall('./data')
        data = CIFAR10()
        classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
        trainLoader = DataLoader(data.trainset, batch_size=4, shuffle=True, num_workers=2)
        testLoader = DataLoader(data.testset, batch_size=4, shuffle=False, num_workers=2)
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
                if sum%100 == 0:
                    print(sum)
                '''
                if sum == 500:
                    break
                '''
                sum += 1
                global cnt
                cnt+=1
                images, labels = data
                images = images.to("cpu")
                labels = labels.to("cpu")
                specialist_idx = np.random.randint(num_vs)
                outputs = net(images, specialist_idx)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum()
                loss += criterion(outputs,labels).mean()
                if need_recall!=None:
                    P += (labels == need_recall).sum()
                    for i in range(len(labels)):
                        if predicted[i] == labels[i] and labels[i] == need_recall:
                            TP+=1
        loss /= len(testLoader)
        print('10000张测试集中的准确率为: %d %%' % (100 * correct / total))
    except Exception as e:
        logging.error(e)
        logging.error(traceback.format_exc())
        print(e)
        return -1
    res = []
    res.append(len(testLoader)*4)
    res.append((correct / total).item())
    if need_loss != None:
        res.append((loss.item()))
    else:
        res.append(-1)
    if need_recall != None:
        if P == 0:
            res.append(-1)
        else:
            res.append((TP/P).item())
    else:
        res.append(-1)
    return res


if __name__ == '__main__':
    '''x = np.load("mnist_testx.npy")
    x=x.reshape((-1,784))
    x = x[:10]
    np.save("mnist_testx.npy",x)
    y = np.load("mnist_testy.npy")
    y = y[:10]
    #y = np_utils.to_categorical(y, 10)
    np.save("mnist_testy.npy", y)'''
    print(0)
    print(sys.path)
    res1 = test_keras("mnist_testx.npy","mnist_testy.npy","mnist_model.h5",True,1)
    print(res1)
    res2 = test_pytorch("./data/cifar-10-python.tar.gz",'./model/final_cifar10_bn343.pth.tar','./etc/cifar10_bn.json',True,1)
    print(res2)