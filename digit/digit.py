# -*- coding: utf-8 -*-
from sklearn.datasets import fetch_mldata
from sklearn.neighbors import KNeighborsClassifier
from collections import defaultdict
from itertools import izip
import cPickle as pickle
import time
import numpy
import logging


LOGLEVEL = logging.INFO
logging.basicConfig()
logger = logging.getLogger("digit")
logger.setLevel(LOGLEVEL)


class DigitClassifier(object):
    """
    A digit classifier based on a K-Nearest Neighbors classifier.
    """
    def __init__(self, noise_threshold=3.0):
        self.classifier = None

    def train(self, features, target):
        logger.info("Train set has {} items".format(len(features)))
        logger.info("Train set has {} features".format(len(features[0])))
        self.classifier = KNeighborsClassifier(5, algorithm="brute",
                                               metric="cosine")
        logger.info("Starting to train...")
        start = time.time()
        self.classifier.fit(features, target)
        logger.info("Training fineshed. It took {} seconds".format(
                                                        time.time() - start))

    def __call__(self, img):
        return self.classify(img)

    def classify(self, img):
        if (not isinstance(img, numpy.ndarray) or
            str(img.dtype) != "uint8" or
            img.shape != (400,)):
            raise ValueError("`img` is expected to be a numpy.ndarray of type "
                             "uint8 and shape (400, ). Ie: a gray-scale "
                             "20x20 image. Aditionally, for the sake of "
                             "precision the image is expected not to have any"
                             "'white' margins around it.")
        return int(self.classifier.predict(img)[0])

    def batch_classify(self, batch):
        img = batch[0]
        if (not isinstance(img, numpy.ndarray) or
            str(img.dtype) != "uint8" or
            img.shape != (400,)):
            raise ValueError("`img` is expected to be a numpy.ndarray of type "
                             "uint8 and shape (400, ). Ie: a gray-scale "
                             "20x20 image. Aditionally, for the sake of "
                             "precision the image is expected not to have any"
                             "'white' margins around it.")
        return self.classifier.predict(batch)

    def _all_options(self, img):
        return zip(self.classifier.predict_proba(img)[0],
                   self.classifier.classes_)

    @classmethod
    def load(cls, path):
        thing = pickle.load(open(path))
        if not isinstance(thing, cls):
            raise ValueError("Wrong type in pickled file")
        return thing

    def save(self, path):
        pickle.dump(self, open(path), pickle.HIGHEST_PROTOCOL)


def generate_basic_dataset():
    # FIXME put this somewhere else
    data_home = "/home/rafael/media/sklearn-data"
    logger.info("Training with MNIST dataset")
    dataset = fetch_mldata('MNIST original', data_home=data_home)
    #dataset = enriquecer(dataset)
    # Pedro de aca para arriba

    data = numpy.array(
        [row.reshape(28, 28)[5:25, 5:25].reshape(20 * 20)
                 for row in dataset.data])
    N = 60000
    features = data[:N]
    target = dataset.target[:N]
    test_features = data[N:]
    test_target = dataset.target[N:]
    return features, target, test_features, test_target


def evaluate(classifier, data, gold):
    confusion = defaultdict(int)
    N = 1000
    n = 0
    hit = 0
    while n < len(data):
        batch = data[n:n + N]
        goldbatch = gold[n: n + N]
        n += N
        test = classifier.batch_classify(batch)
        for testvalue, truevalue in izip(test, goldbatch):
            testvalue = int(testvalue)
            truevalue = int(truevalue)
            if testvalue == truevalue:
                hit += 1
            else:
                confusion[(truevalue, testvalue)] += 1
    return float(hit) / len(data), confusion
