# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import jieba
import json
from trick import filter_words
from variable import *


def document(participle_path, output_path, stop_words_path):
    with open(participle_path, 'r') as participle_file:
        participle_data = json.loads(participle_file.read())
    with open(stop_words_path, 'r') as stop_words_data:
        stop_words = set([line.strip() for line in stop_words_data.readlines()])
    document_index = []
    feature_index = {}
    label = []
    index_up = 0
    for i, row in enumerate(participle_data):
        temp = []
        label.append(row[1])
        for word in row[2:]:
            # stop words -----
            # word = word.encode('utf-8')
            # if word in stop_words:
            #     continue
            # if word in filter_words:
            #     continue
            if word not in feature_index:
                feature_index[word] = index_up
                index_up += 1
            word_index = feature_index[word]
            # 重复词 -----
            # if word_index not in temp:
            temp.append(word_index)
        document_index.append(temp)
        # if i > 100:
        #     break
        print i
    with open(output_path, 'w') as write_file:
        write_file.write(json.dumps({'word_count': index_up,
                                     'document': document_index,
                                     'label': label}))


def participle_file(data_path, participle_data):
    with open(data_path, 'r') as data:
        for i, row in enumerate(data):
            row_data = row.split('\t')
            part_word_gen = jieba.cut(row_data[-1], cut_all=False)
            w = int(row_data[1]) if len(row_data) is 3 else 0
            temp = [int(row_data[0]), w]
            for word in part_word_gen:
                temp.append(word.encode('utf-8'))
            participle_data.append(temp)
            print i


def participle(training_80w_path, test_20w_path, output_path):
    participle_data = []
    participle_file(training_80w_path, participle_data)
    participle_file(test_20w_path, participle_data)
    with open(output_path, 'w') as write_file:
        write_file.write(json.dumps(participle_data))


if __name__ == '__main__':
    training_path = os.getcwd() + '/../data/training_80w.txt'
    test_path = os.getcwd() + '/../data/test_20w.txt'
    participle_file_path = os.getcwd() + '/../data/participle/precision.json'
    document_file_path = os.getcwd() + '/../data/document/precision_stop_rep.json'
    stop_words_path = os.getcwd() + '/../data/stop_words.txt'
#    participle(training_path, test_path, participle_file_path)
    document(participle_file_path, document_file_path, stop_words_path)
