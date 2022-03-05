# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 12:12
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

import jwt
import datetime


class SimpleAuth():
    # 签名秘钥
    secret = 'super-man$&123das%qzq'
    # iss: 该JWT的签发者，是否使用是可选的；
    iss = 'xiaozhongtongxue'
    aud = 'www.xiaozhong.com'

    def __init__(self):
        pass

    # 1000天有效期
    @classmethod
    def create_token_by_data(cls, sub='', data={}, scopes=['open'], exp_time=60 * 60 * 24 * 5):
        """
        生成对应的JWT的token值
        :param sub:    参数名称
        :param data:      参与签名的参数信息
        :param secret:   是否要求进行空检测，True必须检测
        :param exp_time:  token过期时间，按秒来计算
        :return:        返回处理后的参数
        """
        if not data:
            return False, {'access_token': '', 'meg': '需要签名信息不能为空'}

        payload = {
            "iss": cls.iss,  # iss: 该JWT的签发者，是否使用是可选的；
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=exp_time),  # 什么时候过期，这里是一个Unix时间戳，是否使用是可选的；
            "iat": datetime.datetime.utcnow(),  # 在什么时候签发的(UNIX时间)，是否使用是可选的；
            "aud": cls.aud,  # 接收该JWT的一方，是否使用是可选的；#  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
            "sub": sub,  # sub: 该JWT所面向的用户，是否使用是可选的；
            "scopes": scopes,  # 用户授权的作用域，使用逗号（,）分隔
            "data": data
        }
        # 不参与进行签名计算
        if not sub:
            payload.pop('sub')
        # token生成处理
        token = jwt.encode(payload, cls.secret, algorithm='HS256')
        # 返回授权token
        return True, token

    @classmethod
    def verify_bearer_token(cls, ischecck_sub=False, sub_in='', token=''):
        #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
        try:
            payload = jwt.decode(token, cls.secret, audience=cls.aud, algorithms=['HS256'])
            if ischecck_sub and sub_in != '':
                sub = payload['sub']
                if sub != sub_in:
                    return False, "无效的Token"

            if payload and ('data' in payload):
                # 验证通过返回对应的参与签名的字段信息
                return True, payload['data']
            else:
                raise jwt.InvalidTokenError

        except jwt.ExpiredSignatureError:
            return False, "Token过期"

        except jwt.InvalidTokenError:
            return False, "无效的Token"
        except:
            return False, "无效的Token"

    @classmethod
    def verify_bearer_token_state(cls, ischecck_sub=False, sub_in='', token=''):
        #  如果在生成token的时候使用了aud参数，那么校验的时候也需要添加此参数
        try:
            payload = jwt.decode(token, cls.secret, audience=cls.aud, algorithms=['HS256'])
            if ischecck_sub and sub_in != '':
                sub = payload['sub']
                if sub != sub_in:
                    return False, 1, "无效的Token"

            if payload and ('data' in payload):
                # 验证通过返回对应的参与签名的字段信息
                return True, 0, payload['data']
            else:
                raise jwt.InvalidTokenError

        except jwt.ExpiredSignatureError:
            return False, 2, "Token过期"

        except jwt.InvalidTokenError:
            return False, 1, "无效的Token"
        except:
            return False, 1, "无效的Token"











