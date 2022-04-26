from keras import models
import numpy as np
from keras.utils import np_utils


# help(models)
def test_model(model_path,testx_path, testy_path):
    try:
        model = models.load_model(model_path)
        testx = np.load(testx_path)
        testy = np.load(testy_path)
        if (len(testx) != len(testy)):
            return -1,-1
    # testx = testx.reshape((-1,784))

        score = model.evaluate(testx, testy)
    except Exception as e:
        return -1,-1
    return len(testx), score[1]
