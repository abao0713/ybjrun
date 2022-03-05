# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 11:52
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------


from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class GlobalQuestyMiddleware(BaseHTTPMiddleware):


    async def dispatch(self, request: Request, call_next):
        # 给当前的app这是当前的请求上下文对象
        request.app.state.curr_request = request
        response = await call_next(request)
        # 请求之后响应体
        return response











