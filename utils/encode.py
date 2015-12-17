# -*- coding:utf-8 -*-
__author__ = 'chen xi'


def encode_list_to_utf8(list_data):
    ret = []
    for i, x in enumerate(list_data):
        ret.append(x.encode('utf-8'))
    return ret


def encode_to_utf8(json_data):
    """
    把 json 中的 unicode 编码转化为 utf-8 编码
    递归转化
    :param json_data: json 数据
    :return: 相应的 utf-8 编码
    """
    if isinstance(json_data, dict):
        for k, v in json_data.iteritems():
            if isinstance(v, dict):
                encode_to_utf8(v)
            elif isinstance(v, list):
                for i in v:
                    encode_to_utf8(i)
            elif isinstance(k, unicode) or isinstance(v, unicode):
                try:
                    if isinstance(k, unicode):
                        json_data.pop(k)
                        json_data[k.encode('utf-8')] = \
                            v.encode('utf-8') if isinstance(v, unicode) else v
                    else:
                        json_data[k] = v.encode('utf-8')
                except Exception, e:
                    print e
    elif isinstance(json_data, list):
        for i in json_data:
            encode_to_utf8(i)


def is_all_alphabet(string):
    """
    判断一个 utf-8 编码的字符串中的每个字符是否属于如下范围:
    utf-8: 0x00 <= alphabet <= 0x7f
    :param string: utf-8 的字符串
    :return: True | Flase
    """
    for x in string:
        if ord(x) < 0 or ord(x) > 0x7f:
            return False
    return True

