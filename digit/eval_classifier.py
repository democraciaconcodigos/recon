# -*- coding: utf-8 -*-
from digit import AccurateDigitClassifier, FastDigitClassifier, \
                  generate_basic_dataset, evaluate, _entropy
import numpy
import time

if __name__ == "__main__":
    cls = AccurateDigitClassifier()
    #cls = FastDigitClassifier()
    features, target, test_features, test_target = \
        generate_basic_dataset(shuffle=True)
    #cls.train(features[:10000], target[:10000])
    print "Train size      {}".format(len(features))
    print "Evaluation size {}".format(len(test_features))
    print "Using {} classification algorithm".format(cls.classifier)
    cls.train(features, target)
    test_target = test_target#[:1000]
    test_features = test_features#[:1000]

    start = time.time()
    score, confusion = evaluate(cls, test_features, test_target)
    print "Accuracy {:.4f}%".format(100 * score)
    end = time.time()
    print "Eval time {:.4f}s".format(end - start)
    confusion = sorted(confusion.iteritems(), key=lambda x: -len(x[1]))
    print "Biggest sources of confusion:"
    template = "\t{:<5} times guessed {} but was {}, mean entropy = {}"
    for (gold, test), xs in confusion[:20]:
        entro = []
        try:

            for img in xs:
                probs = [p for _, p in cls.classify_with_probabilities(img)]
                #print "\t\t", probs
                entro.append(_entropy(probs))
        except:
            pass
        print template.format(len(xs), test, gold, numpy.array(entro).mean())
