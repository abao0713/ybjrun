# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 11:53
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

from time import perf_counter

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from apps.config.config import auth as auth_conf
from apps.utils.json_response import ForbiddenException, InvalidTokenException, ExpiredTokenException, JSONResponse
from apps.extensions.jwt.simple_auth import SimpleAuth as Auth
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class AuthMiddleware(BaseHTTPMiddleware):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 认证的形式 1：使用默认的，2 使用自定义的
        self.auth_type = 2

    def check_auth_token(self, request):
        '''
        第一步：检测URL地址和携带认证请求头字段信息
        :param request:
        :return:
        '''
        # 如果是使用系统自带的认证的虎，它的需要的认证请求头是必须是Authorization的这个的，当然也可以自定义，不过还不知道咋玩
        while_auth_ulr = auth_conf.ADMIN_WHILE_ROUTE

        # 只有不在白名单的地址需要进行认证的授权的校验
        if request.url.path not in while_auth_ulr and 'sys/randomImag' not in request.url.path and 'docs' not in request.url.path:
            if self.auth_type == 1:
                token = request.headers.get('Authorization', None)
                if not token:
                    return ForbiddenException()
            else:
                # 从头部提取关键的授权码信息
                token = request.headers.get('X-Access-Token', None)
                if not token:
                    # 从get里面进行提取
                    return ForbiddenException()
                    # 下面这种方式，会到全局异常捕获那进行处理
                    # raise HTTPException(HTTP_400_BAD_REQUEST, 'Invalid token')

            return token

    def authenticate_credentials(self, token):
        '''
        第2步：检测URL地址和携带认证请求头字段信息
        :param token:
        :return:
        '''
        isok, state, token_userinfo_result = Auth.verify_bearer_token_state(token=token)
        if not isok and state == 1:
            return InvalidTokenException()
        if not isok and state == 2:
            return ExpiredTokenException()

        return token_userinfo_result

    async def authenticate_credentials_user_info(self, token_userinfo_result):
        '''
        进行TOken内部的包含的用户信息的验证
        :param token:
        :return:
        '''
        isok, isstatus = False, 2

        if not isok:
            return ForbiddenException(msg='该用户已经不存在,请联系管理员！')
        # 用户状态(1-正常,2-冻结)
        # if isstatus.get('status') == 2:
        #     return ForbiddenException(msg='该用户已经被冻结,请联系管理员！')

    async def dispatch(self, request: Request, call_next):
        #    # ---协程对象的返回-使用方法封装后---返回值的处理需要使用这样方式进行---注意返回的时候处理
        #      if isinstance(token_result, JSONResponse):
        #
        #             return token_result
        # 1：检测是否协调认证信息，没有则返回错误提示，有则返回对应的Token的值


        # 如果是使用系统自带的认证的虎，它的需要的认证请求头是必须是Authorization的这个的，当然也可以自定义，不过还不知道咋玩
        while_auth_ulr = auth_conf.ADMIN_WHILE_ROUTE

        # print('while_auth_ulr',while_auth_ulr)

        # 只有不在白名单的地址需要进行认证的授权的校验
        # print("鉴权出来11111111111111111")
        # print('aaaaaaaaawhile_auth_ulr', while_auth_ulr)

        if request.scope["method"]!='OPTIONS' and request.url.path not in while_auth_ulr and 'sys/randomImag' not in request.url.path and 'docs' not in request.url.path:
            if self.auth_type == 1:
                token = request.headers.get('Authorization', None)
                if not token:
                    return ForbiddenException()
            else:
                # 从头部提取关键的授权码信息
                # print("鉴权出来11111111111111111")
                token = request.headers.get('X-Access-Token', None)
                # print("鉴权出来11111111111111111",token)
                if not token:
                    # 从get里面进行提取
                    return ForbiddenException()
            isok, state, token_userinfo_result = Auth.verify_bearer_token_state(token=token)
            if not isok and state == 1:
                return InvalidTokenException()
            if not isok and state == 2:
                return ExpiredTokenException()

            # 写入当前请求上下的当前对象
            request.state.token_userinfo_result = token_userinfo_result


        response = await call_next(request)

        return response











