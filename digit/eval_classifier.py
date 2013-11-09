# -*- coding: utf-8 -*-
from digit import DigitClassifier, generate_basic_dataset, evaluate
import time

if __name__ == "__main__":
    cls = DigitClassifier()
    features, target, test_features, test_target = generate_basic_dataset()
    cls.train(features, target)
    test_target = test_target[:100]
    test_features = test_features[:100]

    #print cls.classify(test_features[4000])

    evaluate(cls, test_features, test_target)
    print "Train size      {}".format(len(features))
    print "Evaluation size {}".format(len(test_features))
    start = time.time()
    score, confusion = evaluate(cls, test_features, test_target)
    print "Accuracy {:.4f}%".format(100 * score)
    end = time.time()
    print "Eval time {:.4f}s".format(end - start)
    confusion = sorted(confusion.iteritems(), key=lambda x: -x[1])
    print "Biggest sources of confusion:"
    for (gold, test), count in confusion[:10]:
        print "\t{:<5} times guessed {} but was {} ".format(count, test, gold)