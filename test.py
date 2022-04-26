import s3
import deploy
import predict
import os
import numpy as np
import json
from keras.utils import np_utils

download_path = "./download/"
s3modelname = "mnist_model.h5"
s3testxname = "mnist_testx.npy"
s3testyname = "mnist_testy.npy"
#s3modelname = s3.upload_data("mnist_model.h5","mnist_model.h5","model")
print("model updated")
#s3testxname = s3.upload_data("mnist_testx.npy","mnist_testx.npy","dataset")
print("testx updated")
#s3testyname = s3.upload_data("mnist_testy.npy","mnist_testy.npy","dataset")
print("testy updated")

modelname = download_path+"mnist_model.h5"
testxname = download_path+"mnist_testx.npy"
testyname = download_path+"mnist_testy.npy"

s3.download_data(modelname,s3modelname,"model")
print("model downloaded")
s3.download_data(testxname,s3testxname,"dataset")
print("testx downloaded")
s3.download_data(testyname,s3testyname,"dataset")
print("testy downloaded")
testx = np.load(testxname)
print(testx.shape)
testy = np.load(testyname)
testx = testx.reshape((-1,784))
testy = np_utils.to_categorical(testy, 10)
endpoint = "mymnistmodel-predict-endpoint"
endpoint = deploy.deploy("mymnistmodel2","s3://modelplexdata/model/mnist_model.h5","keras-cpu")
print("model deployed")
batch_size = 1
image = testx
image = image / 128 - 1
image = np.concatenate([image[np.newaxis, :, :]] * batch_size)
print(image.shape)
body = json.dumps({"instances": image.tolist()})
res = predict.predict(body,testy,endpoint,'application/json')
print(res)

os.remove(modelname)
os.remove(testxname)
os.remove(testyname)
print("finished")