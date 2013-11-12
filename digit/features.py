# -*- coding: utf-8 -*-
import numpy


def shift_left(img):
    img = img.reshape(28, 28)
    a = img[:, 1:]
    b = img[:, -1].reshape(28, 1)
    return numpy.hstack((a, b))


def shift_up(img):
    a = img[1:, :]
    b = img[-1, :].reshape(1, 28)
    return numpy.vstack((a, b))


def sign_change(img):
    img = img.reshape(28, 28)
    top = numpy.bitwise_xor(img, shift_up(img))
    top = [top[:, i].sum() / 255 for i in xrange(img.shape[1])]
    side = numpy.bitwise_xor(img, shift_left(img))
    side = [side[i, :].sum() / 255 for i in xrange(img.shape[1])]
    return numpy.array(top), numpy.array(side)


def side_nz_distance(img):
    img = img.reshape(28, 28)
    left = []
    right = []
    for row in img:
        nz = row.nonzero()[0]
        if len(nz) == 0:
            left.append(0)
            right.append(0)
        else:
            left.append(28 - nz[0])
            right.append(nz[-1])

    left = numpy.array(list(x / 28.0 for x in left))
    right = numpy.array(list(x / 28.0 for x in right))
    return left, right


def reduce_range(data):
    assert len(data) == 28
    xs = []
    for i, j in [(5, 11), (11, 18), (18, 24)]:
        xs.append(data[i:j].mean())
    return numpy.array(xs)
