# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 10:10
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

from apps.config.config import docsconf
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status, Request


def create_app(env):
    app = FastAPI(
        title=docsconf.TITLE,
        description=docsconf.DESC,
        version="V1.0.0",
        # debug 是否再返回结果里面显示错误异常信息
        debug=False,
        docs_url=docsconf.DOCS_URL,
        openapi_url=docsconf.OPENAPI_URL,
        redoc_url=docsconf.REDOC_URL,
        openapi_tags=docsconf.TAGS_METADATA,
        servers=docsconf.SERVERS)

    register_global_logger(app)  # 注册日志处理记录初始化信息
    register_global_exception(app)  # 注册全局异常捕获信息
    register_global_cors(app)  # 全局配置跨域设置
    register_global_middleware(app)  # 注册全局中间件的注册
    register_global_event(app)  # 注册全局的启动和关闭事件
    # register_global_ext_plugs(app)  # 注册所有自定义的或者第三的扩展插件

    # =====================PS=====================
    # 如果需要开启日志记录--优先级最高！必须在如有开始注册之前进行注册
    # =====================PS=====================
    register_global_app_contexr_logger_route(app)  # app注册的路由也加上日志记录
    # self.register_global_include_router()  # 批量导入注册路由
    register_global_health_check(app)  # 默认注册开启健康检测的URL检测

    register_global_websocket_router(app)  # 注册websocketAPI
    register_global_include_router(app)  # 批量导入注册路由

    # PS:如果想看到打印的所有的地址就需要把注册两次启动的是才看到！！！如果不行看可以不用注册两侧，路由依然注册生效
    register_global_include_router(app)  # 批量导入各个模块的下所有的路由信息
    # self.register_global_include_router()  # 批量导入各个模块的下所有的路由信息

    return app

def register_global_logger(app):
    '''
    处理日志的【】配置初始化操作
    :param app:
    :return:
    '''
    # 引入函数和对应的日对象-在当前的APPS目录下建立日志收集管理目录
    import os
    from apps.extensions.logger import creat_customize_log_loguru, logger
    creat_customize_log_loguru(pro_path=os.path.split(os.path.realpath(__file__))[0])

def register_global_ext_plugs(app):
    pass
    # # 初始化第三的请求HTTP客户端对象
    from apps.ext.asynhttp import async_client
    async_client.init_app(app)
    #
    # 初始化redis客户端
    from apps.ext.pooled_postgresql import sync_pooled_postgresql_client
    sync_pooled_postgresql_client.init_app(app)

    # 初始化同步redis客户端对象
    from apps.ext.redis.syncredis2 import sync_redis_client
    sync_redis_client.init_app(app)

    # 创建队列
    # sync_rabbit_client.creat_dead_exchange_and_queue()

def register_global_event(app):
    pass
    # 注册App结束的时候，清楚相关的异步任务

def register_include_router(app):
    '''
    导入路由模块
    :param app:
    :return:
    '''
    pass

def register_global_middleware(app):
    '''
    配置中间件
     # 中间件执行的顺序是，谁先注册,谁就再最内层，它的再后一个注册，就再最外层
    :param app:
    :return:
    '''
    pass
    from apps.middleware.global_auth import AuthMiddleware
    # self.startge.add_middleware(AuthMiddleware)
    from apps.middleware.global_requests import GlobalQuestyMiddleware
    app.add_middleware(GlobalQuestyMiddleware)

    # 如果是也要记录用户提交的参数信息的是错误的情况也好分析的，把日志放最外层
    # self.app.add_middleware(LoggingMiddleware)
    # from apps.middleware.global_errer import GlobalErrorMiddleware
    # self.startge.add_middleware(GlobalErrorMiddleware)

def register_global_cors(app):
    '''
    处理全局的跨域
    :param app:
    :return:
    '''
    pass
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def register_global_exception(app):
    '''
    配置我们的所有的异常
    :param app:
    :return:
    '''
    pass
    from apps.extensions.exception import ApiExceptionHandler
    ApiExceptionHandler().init_app(app)

def register_global_app_contexr_logger_route(app):
    '''
    是否全局的配注所有的A使用APP直接注册的方式注册的路由进行日志记录
    :return:
    '''
    pass
    # 要开启日志的激励的话，这个地方需要执行初始化化追踪的ID
    from apps.extensions.logger import LoggerRouteTrace
    app.router.route_class = LoggerRouteTrace

def register_global_health_check(app):
    pass
    @app.get('/check', tags=['默认开启的健康检查'])
    async def health_check(re: Request):
        from apps.extensions.logger import LoggerRouteTrace, logger
        LoggerRouteTrace.sync_trace_add_log_record_norequest(event_type='预扣库存信息', msg='你也打好的哈')
        # ContextLogerRoute.sync_trace_add_log_record(re,event_type='预扣库存信息222', msg='你也打好的哈')

        return 'ok242342'

def register_global_include_router(app):
    pass
    '''
    导入路由模块
    :param app:
    :return:
    '''
    pass
    # from apps.modules import init_routes
    # init_routes(app)

def mount_static_files(app):
    # 装载静态目录
    from starlette.staticfiles import StaticFiles
    import os
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # 静态文件目录
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    app.mount("/static", StaticFiles(directory=STATIC_DIR))

def register_global_websocket_router(app):
    @app.websocket("/nw/websocket/{userid}")
    async def websocket_userid(websocket: WebSocket, userid: str):
        # 等待连接
        await websocket.accept()
        # 处理链接
        while True:
            # 接收发送过来的数据信息
            data = await websocket.receive_text()
            # 把接收过来的数据再一次的发送回去
            await websocket.send_text(f"ok")
            # 如果存在参数信息











