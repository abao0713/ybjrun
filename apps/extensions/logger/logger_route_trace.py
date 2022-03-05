# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 11:34
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

from time import perf_counter
from loguru import logger
from fastapi import APIRouter, FastAPI, Request, Response, Body
from fastapi.routing import APIRoute
from typing import Callable, List
from fastapi.responses import Response
from apps.utils import json_helper
import uuid
import shortuuid
from datetime import datetime
from user_agents import parse
from urllib.parse import parse_qs


# 因为Fastapi无法再中间二次消费请求的问题，只能通过自定义的路由的方式来进行日志的记录

class LoggerRouteTrace(APIRoute):
    pass
    # 配置需要特殊记录的请求的头的值的信息
    nesss_access_heads_keys = []

    @staticmethod
    def sync_trace_add_log_record_norequest( event_type='', msg={}, remarks=''):
        """
        验证用户是否有对应接口权限
        """

        def sync_trace_add_log_record(request: Request, event_type='', msg={}, remarks=''):
            # 查询拥有权限的user
            pass
            # 如果没有这个标记的属性的，说明这个接口的不需要记录啦！
            if hasattr(request.state, 'traceid'):
                # 自增编号索引序
                trace_links_index = request.state.trace_links_index = getattr(request.state, 'trace_links_index') + 1
                log = {
                    # 自定义一个新的参数复制到我们的请求上下文的对象中
                    'traceid': getattr(request.state, 'traceid'),
                    # 定义链路所以序号
                    'trace_index': trace_links_index,
                    # 时间类型描述描述
                    'event_type': event_type,
                    # 日志内容详情
                    'msg': msg,
                    # 日志备注信息
                    'remarks': remarks,

                }
                #  为少少相关记录，删除不必要的为空的日志内容信息，
                if not remarks:
                    log.pop('remarks')
                if not msg:
                    log.pop('msg')
                try:
                    log_msg = json_helper.dict_to_json_ensure_ascii(log)  # 返回文本
                    logger.info(log_msg)
                except:
                    logger.info(getattr(request.state, 'traceid') + '：索引：' + str(
                        getattr(request.state, 'trace_links_index')) + ':日志信息写入异常')

        return sync_trace_add_log_record

    @staticmethod
    def sync_trace_add_log_record(request: Request, event_type='', msg={}, remarks=''):
        '''

        :param event_type: 日志记录事件描述
        :param msg: 日志记录信息字典
        :param remarks: 日志备注信息
        :return:
        '''

        # 如果没有这个标记的属性的，说明这个接口的不需要记录啦！
        print("收到收到货", hasattr(request.state, 'traceid'))
        if hasattr(request.state, 'traceid'):
            # 自增编号索引序
            trace_links_index = request.state.trace_links_index = getattr(request.state, 'trace_links_index') + 1
            log = {
                # 自定义一个新的参数复制到我们的请求上下文的对象中
                'traceid': getattr(request.state, 'traceid'),
                # 定义链路所以序号
                'trace_index': trace_links_index,
                # 时间类型描述描述
                'event_type': event_type,
                # 日志内容详情
                'msg': msg,
                # 日志备注信息
                'remarks': remarks,

            }
            #  为少少相关记录，删除不必要的为空的日志内容信息，
            if not remarks:
                log.pop('remarks')
            if not msg:
                log.pop('msg')
            try:
                log_msg = json_helper.dict_to_json_ensure_ascii(log)  # 返回文本
                logger.info(log_msg)
            except:
                logger.info(getattr(request.state, 'traceid') + '：索引：' + str(
                    getattr(request.state, 'trace_links_index')) + ':日志信息写入异常')

    # 封装一下关于记录序号的日志记录用于全链路的日志请求的日志
    @staticmethod
    async def async_trace_add_log_record(request: Request, event_type='', msg={}, remarks=''):
        '''

        :param event_type: 日志记录事件描述
        :param msg: 日志记录信息字典
        :param remarks: 日志备注信息
        :return:
        '''

        # print("我当前的请求ID:",request.app.state.curr_request,id(request.app.state.curr_request))
        # print("我当前的请求ID:", request,id(request))
        #
        # print("我当前的请求ID:", request.app.state.curr_request.state.ssss)
        # print("我当前的请求ID:", request.state.ssss)

        # 如果没有这个标记的属性的，说明这个接口的不需要记录啦！
        if hasattr(request.state, 'traceid'):
            # 自增编号索引序
            trace_links_index = request.state.trace_links_index = getattr(request.state, 'trace_links_index') + 1
            log = {
                # 自定义一个新的参数复制到我们的请求上下文的对象中
                'traceid': getattr(request.state, 'traceid'),
                # 定义链路所以序号
                'trace_index': trace_links_index,
                # 时间类型描述描述
                'event_type': event_type,
                # 日志内容详情
                'msg': msg,
                # 日志备注信息
                'remarks': remarks,

            }
            #  为少少相关记录，删除不必要的为空的日志内容信息，
            if not remarks:
                log.pop('remarks')
            if not msg:
                log.pop('msg')
            try:
                log_msg = json_helper.dict_to_json_ensure_ascii(log)  # 返回文本
                logger.info(log_msg)
            except:
                logger.info(getattr(request.state, 'traceid') + '：索引：' + str(
                    getattr(request.state, 'trace_links_index')) + ':日志信息写入异常')

    async def _init_trace_start_log_record(self, request: Request):
        '''
        请求记录初始化
        :return:
        '''

        # 配置当前的清除的上下文对象
        # request.app.
        self.request = request

        path_info = request.url.path
        if path_info not in ['/favicon.ico'] and 'websocket' not in path_info:
            if request.method != 'OPTIONS':
                # 追踪索引
                request.state.trace_links_index = 0
                # 追踪ID
                # request.traceid = str(uuid.uuid4()).replace('-', '')
                request.state.traceid = shortuuid.uuid()
                # 计算时间
                request.state.start_time = perf_counter()
                # 获取请求来源的IP,请求的方法
                ip, method, url = request.client.host, request.method, request.url.path
                # print('scope', request.scope)
                # 先看表单有没有数据：
                try:
                    body_form = await request.form()
                except:
                    body_form = None

                body = None
                try:
                    body_bytes = await request.body()
                    if body_bytes:
                        try:
                            body = await  request.json()
                        except:
                            pass
                            if body_bytes:
                                try:
                                    body = body_bytes.decode('utf-8')
                                except:
                                    body = body_bytes.decode('gb2312')
                except:
                    pass

                # 从头部里面获取出对应的请求头信息，用户用户机型等信息获取
                user_agent = parse(request.headers["user-agent"])
                browser = user_agent.browser.version
                if len(browser) >= 2:
                    browser_major, browser_minor = browser[0], browser[1]
                else:
                    browser_major, browser_minor = 0, 0

                user_os = user_agent.os.version
                if len(user_os) >= 2:
                    os_major, os_minor = user_os[0], user_os[1]
                else:
                    os_major, os_minor = 0, 0

                log_msg = {
                    # 'headers': str(request.headers),
                    # 'user_agent': str(request.user_agent),
                    # 记录请求头信息----如果需要特殊的获取某些请求的记录则做相关的配置即可
                    'headers': [request.headers.get(i, '') for i in
                                self.nesss_access_heads_keys] if self.nesss_access_heads_keys else None,
                    # 记录请求URL信息
                    "useragent":
                        {
                            "os": "{} {}".format(user_agent.os.family, user_agent.os.version_string),
                            'browser': "{} {}".format(user_agent.browser.family, user_agent.browser.version_string),
                            "device": {
                                "family": user_agent.device.family,
                                "brand": user_agent.device.brand,
                                "model": user_agent.device.model,
                            }
                        },
                    'url': url,
                    # 记录请求方法
                    'method': method,
                    # 记录请求来源IP
                    'ip': ip,
                    # 'path': request.path,
                    # 记录请求提交的参数信息
                    'params': {
                        'query_params': parse_qs(str(request.query_params)),
                        'from': body_form,
                        'body': body
                    },
                    # 记录请求的开始时间
                    "ts": f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
                    # 'start_time':  f'{(start_time)}',
                }
                if not log_msg['headers']:
                    log_msg.pop('headers')

                if not log_msg['params']['query_params']:
                    log_msg['params'].pop('query_params')
                if not log_msg['params']['from']:
                    log_msg['params'].pop('from')
                if not log_msg['params']['body']:
                    log_msg['params'].pop('body')
                # 执行写入--日志具体的内容信息
                await self.async_trace_add_log_record(request, event_type='request', msg=log_msg)

    async def _init_trace_end_log_record(self, request: Request, response: Response):

        # https://stackoverflow.com/questions/64115628/get-starlette-request-body-in-the-middleware-context
        # 如果响应图的类型，仅仅记录字符串类型的结尾的日志信息
        if 'image' not in response.media_type and hasattr(request.state, 'traceid'):
            start_time = getattr(request.state, 'start_time')
            end_time = f'{(perf_counter() - start_time):.2f}'
            # 获取响应报文信息内容
            rsp = None
            if isinstance(response, Response):
                rsp = str(response.body, encoding='utf-8')
            log_msg = {
                # 记录请求耗时
                "status_code": response.status_code,
                'cost_time': end_time,
                #  记录请求响应的最终报文信息--eval的作用是去除相关的 转义符号 "\"ok\""===》ok
                'rsp': json_helper.json_to_dict(rsp),
                "ts": f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
            }
            await self.async_trace_add_log_record(request, event_type='response', msg=log_msg)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        # 自定义路由的方式内容
        async def custom_route_handler(request: Request) -> Response:
            # 请求前的处理-日志的初始化操作

            await self._init_trace_start_log_record(request)

            response: Response = await original_route_handler(request)

            # 一个API请求处理完成后的-日志收尾记录
            await self._init_trace_end_log_record(request, response)

            return response

        return custom_route_handler











