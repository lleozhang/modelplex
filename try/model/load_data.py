import torch
from torch.utils.data import DataLoader

import torchvision
import torchvision.transforms as transforms
import tarfile

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

def load_data(data_path):
    print("load data")
    tf = tarfile.open(data_path)
    tf.extractall('./data')
    data = CIFAR10()
    testLoader = DataLoader(data.testset, batch_size=4, shuffle=False, num_workers=2)
    return testLoader