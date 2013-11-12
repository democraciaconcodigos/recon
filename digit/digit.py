# -*- coding: utf-8 -*-

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.decomposition import TruncatedSVD
from sklearn.datasets import fetch_mldata
from collections import defaultdict
from itertools import izip
import cPickle as pickle
import time
import numpy
import logging
import math
from features import sign_change, side_nz_distance, reduce_range


LOGLEVEL = logging.INFO
logging.basicConfig()
logger = logging.getLogger("digit")
logger.setLevel(LOGLEVEL)


class BaseDigitClassifier(object):
    """
    Abstract base class for the digit classifiers on this file
    """
    def train(self, features, target):
        self._check_valid_sample(features[0])
        start = time.time()
        features = self.apply_image_preprocessing(features)
        self.train_dimensionality_reduction(features)
        features = self.apply_dimensionality_reduction(features)
        logger.info("Feature preprocessing took {} seconds".format(
                                                        time.time() - start))
        logger.info("Train set has {} items".format(len(features)))
        logger.info("Train set has {} features".format(len(features[0])))
        logger.info("Starting to train...")
        start = time.time()
        self.classifier.fit(features, target)
        logger.info("Training fineshed. It took {} seconds".format(
                                                        time.time() - start))

    def apply_image_preprocessing(self, batch):
        return batch

    def train_dimensionality_reduction(self, features):
        return features

    def apply_dimensionality_reduction(self, features):
        return features

    def __call__(self, img):
        return self.classify(img)

    def classify(self, img):
        return self.batch_classify([img])

    def batch_classify(self, batch):
        self._check_valid_sample(batch[0])
        batch = self.apply_image_preprocessing(batch)
        batch = self.apply_dimensionality_reduction(batch)
        return map(int, self.classifier.predict(batch))

    def _check_valid_sample(self, img):
        if (not isinstance(img, numpy.ndarray) or
            str(img.dtype) != "uint8" or
            img.shape != (784,)):
            raise ValueError("`img` is expected to be a numpy.ndarray of type "
                             "uint8 and shape (784, ). Ie: a gray-scale "
                             "28x28 image. Aditionally, for the sake of "
                             "precision the image is expected not to have any"
                             "'white' margins around it.")

    def classify_with_probabilities(self, img):
        img = self.apply_image_preprocessing([img])[0]
        img = self.apply_dimensionality_reduction([img])[0]
        return zip(self.classifier.classes_,
                   self.classifier.predict_proba(img)[0])

    @classmethod
    def load(cls, path):
        thing = pickle.load(open(path))
        if not isinstance(thing, cls):
            raise ValueError("Wrong type in pickled file")
        return thing

    def save(self, path):
        pickle.dump(self, open(path), pickle.HIGHEST_PROTOCOL)


class AccurateDigitClassifier(BaseDigitClassifier):
    """
    A digit classifier based on a K-Nearest Neighbors classifier, using
    the raw pixels as features.
    """
    def __init__(self):
        self.classifier = KNeighborsClassifier(5, algorithm="brute",
                                                metric="cosine",
                                                weights="uniform")
        #self.classifier = KNeighborsClassifier(5, algorithm="auto")
        #self.classifier = SVC()
        #self.classifier = GaussianNB()
        #base = DecisionTreeClassifier(min_samples_split=10)
        #self.classifier = AdaBoostClassifier(base, n_estimators=20)

    def train_dimensionality_reduction(self, features):
        self.dimred = TruncatedSVD(80)
        self.dimred.fit(features)

    def apply_dimensionality_reduction(self, features):
        return self.dimred.transform(features)

    """
    def apply_image_preprocessing(self, batch):
        batch = [row.reshape(28, 28)[5:25, 5:25].reshape(20 * 20)
                               for row in batch]
        return numpy.array(batch)
    """


class FastDigitClassifier(BaseDigitClassifier):
    """
    A digit classifier based on Adaboost of random trees using
    a reduced feature set.
    """
    def __init__(self):
        #base = DecisionTreeClassifier(min_samples_split=10)
        #base = algo.fit(train_features, train_target)
        #self.classifier = AdaBoostClassifier(base, n_estimators=20)
        #self.classifier = GaussianNB()
        #self.classifier = SVC(probability=True)
        self.classifier = SVC(probability=True, kernel="linear")
        #self.classifier = LinearSVC()

    def apply_image_preprocessing(self, batch):
        xs = []
        for img in batch:
            top, side = sign_change(img)
            #top = reduce_range(top)
            #side = reduce_range(side)
            left, right = side_nz_distance(img)
            #left = reduce_range(left)
            #right = reduce_range(right)
            feat = numpy.c_[top.reshape(1, len(top)),
                            side.reshape(1, len(side)),
                            left.reshape(1, len(left)),
                            right.reshape(1, len(right))]
            xs.append(feat.ravel())
        return numpy.array(xs)

    def train_dimensionality_reduction(self, features):
        self.dimred = TruncatedSVD(40)
        self.dimred.fit(features)

    def apply_dimensionality_reduction(self, features):
        return self.dimred.transform(features)


def generate_basic_dataset(shuffle=True):
    # FIXME put this somewhere else
    data_home = "/home/rafael/media/sklearn-data"
    logger.info("Training with MNIST dataset")
    dataset = fetch_mldata('MNIST original', data_home=data_home)
    #dataset = enriquecer(dataset)
    # Pedro de aca para arriba

    images = dataset.data
    labels = dataset.target
    if shuffle:
        numpy.random.seed(hash("democraciaconcodigos") % 1234)
        permutation = numpy.random.permutation(len(images))
        images = images[permutation]
        labels = labels[permutation]
    N = (len(images) / 7) * 6
    features = images[:N]
    target = labels[:N]
    test_features = images[N:]
    test_target = labels[N:]
    return features, target, test_features, test_target


def evaluate(classifier, data, gold):
    confusion = defaultdict(list)
    N = 1000
    n = 0
    hit = 0
    while n < len(data):
        batch = data[n:n + N]
        goldbatch = gold[n: n + N]
        n += N
        test = classifier.batch_classify(batch)
        for i, testvalue, truevalue in izip(xrange(len(test)),
                                            test, goldbatch):
            testvalue = int(testvalue)
            truevalue = int(truevalue)
            if testvalue == truevalue:
                hit += 1
            else:
                confusion[(truevalue, testvalue)].append(batch[i])
    return float(hit) / len(data), confusion


def _entropy(probabilities):
    return -sum(p * math.log(p, 2) for p in probabilities if p != 0)
