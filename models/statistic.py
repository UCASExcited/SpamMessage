# -*- coding: utf-8 -*-
__author__ = 'zhsl'
import os
import json


def statistic_trick_words(frequency_path, value_threshold=100):
    with open(frequency_path, 'r') as read_file:
        frequency = json.loads(read_file.read())['frequency']
    trick_words = {}
    for key, value in frequency[1].iteritems():
        if key not in frequency[0] and value > value_threshold:
            trick_words[int(key)] = value
    return trick_words


def have_trick_words(document_row, trick_words, value_threshold):
    for x in document_row:
        if x in trick_words and trick_words[x] > value_threshold:
            return True
    return False


if __name__ == '__main__':
    frequency_path = os.getcwd() + '/../data/frequency/precision_stop_rep.json'
    statistic_trick_words(frequency_path)
