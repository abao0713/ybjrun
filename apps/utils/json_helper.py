# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 11:43
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

import json
import datetime
import decimal


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            return dict(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


def dict_to_json(dict={}):
    return json.dumps(dict, cls=CJsonEncoder)


# 不格式化的输出ensure_ascii==false 输出中文的时候，保持中文的输出
def dict_to_json_ensure_ascii(dict={}, ensure_ascii=False):
    return json.dumps(dict, cls=CJsonEncoder, ensure_ascii=ensure_ascii)


# 格式化排版缩进输出-ensure_ascii==false 输出中文的时候，保持中文的输出
def dict_to_json_ensure_ascii_indent(dict={}, ensure_ascii=False):
    return json.dumps(dict, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)


def obj_to_json(obj, ensure_ascii=False):
    stu = obj.__dict__  # 将对象转成dict字典
    return json.dumps(obj=stu, cls=CJsonEncoder, ensure_ascii=ensure_ascii, indent=4)


def json_to_dict(json_msg):
    dict = json.loads(s=json_msg)
    return dict


def class_to_dict(obj):
    if not obj:
        return None
    is_list = obj.__class__ == [].__class__
    is_set = obj.__class__ == set().__class__

    if is_list or is_set:
        obj_arr = []
        for o in obj:
            dict = {}
            dict.update(o.__dict__)
            obj_arr.append(dict)
        return obj_arr
    else:
        dict = {}
        dict.update(obj.__dict__)
        return dict.get('__data__')











