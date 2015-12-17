# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import jieba
import os
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from utils import encode_to_utf8

filter_words = [' ', '\r\n']
training_path = os.getcwd() + '/../data/training_80w.txt'
output_path = os.getcwd() + '/../data/frequency_junk.json'
stop_words_list_path = os.getcwd() + '/../data/stop_words.txt'


def participle_junk(training_path, output_path, stop_words_list_path):
    with open(stop_words_list_path, 'r') as stop_words_data:
        stop_words = set([line.strip() for line in stop_words_data.readlines()])
    for x in filter_words:
        stop_words.add(x)
    with open(training_path, 'r') as data:
        frequency_junk = {}
        cnt_junk = 0
        for i, row in enumerate(data):
            row_data = row.split('\t')
            if row_data[len(row_data) - 2] == '0':
                continue
            cnt_junk += 1
            part_word_gen = jieba.cut(row_data[-1], cut_all=False)
            for word in part_word_gen:
                word = word.encode('utf-8')
                if word in stop_words:
                    continue
                if word in frequency_junk:
                    frequency_junk[word] += 1
                else:
                    frequency_junk[word] = 1
#            print i, cnt_junk
    with open(output_path, 'w') as write_file:
        write_file.write(json.dumps(frequency_junk))
    return


def sort_by_value(d):
    items = d.items()
    backitems = [[v[1], v[0]] for v in items]
    backitems.sort()
    return [(backitems[i][1], backitems[i][0]) for i in range(0, len(backitems))]


def junk_words_select(frequency_junk_path):
    with open(frequency_junk_path, 'r') as read_file:
        frequency_junk = json.loads(read_file.read())
        encode_to_utf8(frequency_junk)
    frequency_sort = sort_by_value(frequency_junk)
    for key, value in frequency_sort:
        print key, value


def junk_trick(predict, training_path, stop_words_path, training_count):
    with open(stop_words_list_path, 'r') as stop_words_data:
        stop_words = set([line.strip() for line in stop_words_data.readlines()])
    with open(output_path, 'r') as read_file:
        frequency_junk = json.loads(read_file.read())
        encode_to_utf8(frequency_junk)
    for x in filter_words:
        stop_words.add(x)
    with open(training_path, 'r') as data:
        for i, row in enumerate(data):
            if i < training_count or predict[i - training_count]:
                continue
            row_data = row.split('\t')
#            if row_data[len(row_data) - 2] == '0':
#                continue
            part_word_gen = jieba.cut(row_data[-1], cut_all=False)
            for word in part_word_gen:
                word = word.encode('utf-8')
                if word in frequency_junk and frequency_junk[word] == 14017:
                    print row_data[len(row_data) - 2], word
                    predict[i - training_count] = 1
    return


def junk_trick_test(predict, test_path, stop_words_path, training_count):
    with open(stop_words_list_path, 'r') as stop_words_data:
        stop_words = set([line.strip() for line in stop_words_data.readlines()])
    with open(output_path, 'r') as read_file:
        frequency_junk = json.loads(read_file.read())
        encode_to_utf8(frequency_junk)
    for x in filter_words:
        stop_words.add(x)
    with open(test_path, 'r') as data:
        for i, row in enumerate(data):
            row_data = row.split('\t')
            part_word_gen = jieba.cut(row_data[-1], cut_all=False)
            for word in part_word_gen:
                word = word.encode('utf-8')
                if word in frequency_junk and frequency_junk[word] > 40000:
                    predict[i] = 1
    return


if __name__ == '__main__':
#    participle_junk(training_path, output_path, stop_words_list_path)
    junk_words_select(output_path)

