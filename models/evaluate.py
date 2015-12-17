# -*- coding: utf-8 -*-
__author__ = 'zhsl'


def evaluate(label, predict):
    if len(label) != len(predict):
        print 'len error'
        return
    cnf = [[0, 0], [0, 0]]
    for i in range(len(label)):
        cnf[label[i]][predict[i]] += 1
    print cnf
    junk_precision = cnf[1][1] / float(cnf[0][1] + cnf[1][1])
    junk_recall = cnf[1][1] / float(cnf[1][0] + cnf[1][1])
    normal_precision = cnf[0][0] / float(cnf[0][0] + cnf[1][0])
    normal_recall = cnf[0][0] / float(cnf[0][0] + cnf[0][1])
    f_junk = 0.65 * junk_precision + 0.35 * junk_recall
    f_normal = 0.65 * normal_precision + 0.35 * normal_recall
    f = 0.7 * f_junk + 0.3 * f_normal
    print ' --------- confusion matrix ---------'
    print '%8d%8d\n%8d%8d' % (cnf[0][0], cnf[0][1], cnf[1][0], cnf[1][1])
    print ' --------- result ---------'
    print 'junk_precision:\t\t', junk_precision
    print 'junk_recall:\t\t', junk_recall
    print 'normal_precision:\t', normal_precision
    print 'normal_recall:\t\t', normal_recall
    print 'score:', f
    return f

