# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 11:53
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------



from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from apps.response.json_response import *
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import HTTPException as FastapiHTTPException
from fastapi.exceptions import RequestValidationError
from pydantic.errors import *
from apps.extensions.logger import logger
import traceback

class GlobalErrorMiddleware(BaseHTTPMiddleware):


    async def dispatch(self, request: Request, call_next):
        # 给当前的app这是当前的请求上下文对象
        # request.apps.state.curr_request = request
        # response = await call_next(request)
        # # 请求之后响应体
        # return response
        try:
            response = await call_next(request)
        except RequestValidationError as e:
            return await self.validation_exception_handler(request,e)
        except FastapiHTTPException as e:
            return await self.http_exception_handler(request, e)
        except Exception as e:
            return await self.all_exception_handler(request, e)
        else:
            return response

    async def validation_exception_handler(self, request: Request, exc: RequestValidationError):
        # print("参数提交异常错误selfself", exc.errors()[0].get('loc'))
        # 路径参数错误
        # 判断错误类型
        if isinstance(exc.raw_errors[0].exc, IntegerError):
            pass
        elif isinstance(exc.raw_errors[0].exc, MissingError):
            pass
        return ParameterException(http_status_code=400, api_code=400, message='参数校验错误', result={
            "detail": exc.errors(),
            "body": exc.body
        })

    async def all_exception_handler(self, request: Request, exc: Exception):
        '''
        全局的捕获抛出的HTTPException异常，注意这里需要使用StarletteHTTPException的才可以
        :param request:
        :param exc:
        :return:
        '''
        # log_msg = f"捕获到系统错误：请求路径:{request.url.path}\n错误信息：{traceback.format_exc()}"
        if isinstance(exc, StarletteHTTPException) or isinstance(exc, FastapiHTTPException):
            if exc.status_code == 405:
                return MethodnotallowedException()
            if exc.status_code == 404:
                return NotfoundException()
            elif exc.status_code == 429:
                return LimiterResException()
            elif exc.status_code == 500:
                return InternalErrorException()
            elif exc.status_code == 400:
                # 有部分的地方直接的选择使用raise的方式抛出了异常，这里也需要进程处理
                # raise HTTPException(HTTP_400_BAD_REQUEST, 'Invalid token')
                return BadrequestException(msg=exc.detail)

            return BadrequestException()
        else:
            # 其他内部的异常的错误拦截处理
            logger.exception(exc)
            traceback.print_exc()
            return InternalErrorException()

    async def http_exception_handler(self, request: Request, exc: StarletteHTTPException):
        '''
           全局的捕获抛出的HTTPException异常，注意这里需要使用StarletteHTTPException的才可以
           :param request:
           :param exc:
           :return:
           '''
        # 这里全局监听了我们的所有的HTTP响应，包括了200 的也会尽到这里来！
        # print("撒很好收到哈搜地和撒谎的撒22222222222===========",exc)
        # log_msg = f"捕获到系统错误：请求路径:{request.url.path}\n错误信息：{traceback.format_exc()}"

        if exc.status_code == 405:
            return MethodnotallowedException()
        if exc.status_code == 404:
            return NotfoundException()
        elif exc.status_code == 429:
            return LimiterResException()
        elif exc.status_code == 500:
            return InternalErrorException()
        elif exc.status_code == 400:
            # 有部分的地方直接的选择使用raise的方式抛出了异常，这里也需要进程处理
            # raise HTTPException(HTTP_400_BAD_REQUEST, 'Invalid token')
            return BadrequestException(msg=exc.detail)










