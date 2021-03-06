# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import json
import math
import csv
from evaluate import evaluate
from trick import junk_trick, junk_trick_test
from variable import *


def training(training_data, frequency_path):
    document = training_data['document']
    label = training_data['label']
    positive_label = label.count(1)
    p_c = [(end1 - positive_label) / float(end1),
           positive_label / float(end1)]
    frequency = [{}, {}]
    for i, row in enumerate(document):
        frequency_select = frequency[label[i]]
        for x in row:
            if x in frequency_select:
                frequency_select[x] += 1
            else:
                frequency_select[x] = 1
        print i
    with open(frequency_path, 'w') as write_file:
        write_file.write(json.dumps({'frequency': frequency,
                                     'p_c': p_c}))


def probability(row, n_words, frequency, p_c, w):
    p = 0.0
    for x in row:
        x = str(x)
        x_frequency = frequency[w][x] if x in frequency[w] else 0
        p_x_given_c = (x_frequency + 1) / float(n_words)
        p += math.log(p_x_given_c)
    return p + math.log(p_c[w])


def predict(test_data, frequency_path, alpha=0.894):
    with open(frequency_path, 'r') as frequency_file:
        frequency = json.loads(frequency_file.read())
    p_c = frequency['p_c']
    frequency = frequency['frequency']
    test_data = test_data['document']
    n_features = len(frequency)
    ret = [0] * len(test_data)
    n_words = [0] * 2
    for i in range(2):
        for key, value in frequency[i].items():
            n_words[i] += value
    for i, row in enumerate(test_data):
        p_1 = probability(row, n_words[1] + n_features, frequency, p_c, 1)
        p_0 = probability(row, n_words[0] + n_features, frequency, p_c, 0)
        if p_1 > alpha * p_0:
            ret[i] = 1
    return ret


def write_csv(file_path, content):
    with open(file_path, 'w') as write_file:
        writer = csv.writer(write_file)
        for i, x in enumerate(content, start=800001):
            writer.writerow([i, x])


def init_data(document_path):
    with open(document_path, 'r') as data:
        data = json.loads(data.read())
    return {'document': data['document'][:end1], 'label': data['label'][:end1]},\
           {'document': data['document'][end1:end2], 'label': data['label'][end1:end2]}


if __name__ == '__main__':
    document_path = os.getcwd() + '/../data/document/precision_stop_rep.json'
    frequency_path = os.getcwd() + '/../data/frequency/precision_stop_rep.json'
    result_path = os.getcwd() + '/../data/result.csv'
    # init data -----
    training_data, test_data = init_data(document_path)
    # training -----
    # training(training_data, frequency_path)
    # predict -----
    ret = predict(test_data, frequency_path)
    # evaluate -----
    evaluate(test_data['label'], ret)
    training_label = training_data['label']
    print 'training:', training_label.count(1), training_label.count(0), \
        training_label.count(1) / float(len(training_label)), \
        training_label.count(0) / float(len(training_label))
    print 'predict:', ret.count(1), ret.count(0), \
        ret.count(1) / float(len(ret)), \
        ret.count(0) / float(len(ret))
    # write result -----
    write_csv(result_path, ret)
    # alpha ------------
    # max_score = 0.0
    # alpha = []
    # for num in [x / 1000.0 for x in range(890, 910)]:
    #     ret = predict(test_data, frequency_path, alpha=num)
    #     temp = evaluate(test_data['label'], ret)
    #     if temp > max_score:
    #         max_score = temp
    #         alpha = num
    #     print temp, max_score, alpha
    # print alpha
