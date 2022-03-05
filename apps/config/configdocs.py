# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 10:27
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

from functools import lru_cache
from pydantic import BaseSettings
import pprint

pp = pprint.PrettyPrinter(indent=4)


class DocsSettings(BaseSettings):
    """配置类"""
    API_V1_STR: str = ""
    # 文档接口描述相关的配置
    DOCS_URL = API_V1_STR + '/docs'
    REDOC_URL = API_V1_STR + '/redocs'
    # OPENAPI_URL配置我们的openapi，json的地址
    OPENAPI_URL = API_V1_STR + '/openapi_url'
    # 接口描述
    TITLE = "管理系统后台"
    # 首页描述文档的详细介绍信息
    DESC = """
            `斡旋中医馆线上预约系统`
            - 前端：使用 ANT VBEN的框架进行搭建
            - 后端: 同步模式的多线程模式+ 单线程模式的协程模式
            - 技术栈 ：FastAPI+ POSTGRESQL+自制ORM 
        """
    TAGS_METADATA = [
        {
            "name": "后台管理系统",
            "description": "后台所有的公司的相关的权限管理",
        },
        # {
        #     "name": "5G消息管理模块",
        #     "description": "后台所有的公司的相关的权限管理",
        # },
        # {
        #     "name": "你没22",
        #     "description": "aaaa后台所有的公司的相关的权限管理",
        #     "externalDocs": {
        #         "description": "子文档信息",
        #         "url": "https://fastapi.tiangolo.com/",
        #     },
        # },

    ]
    # 配置代理相关的参数信息
    SERVERS = [
        {"url": "/", "description": "本地调试环境"},
        {"url": "https://xx.xx.com", "description": "线上测试环境"},
        {"url": "https://xx2.xx2.com", "description": "线上生产环境"},
    ]


@lru_cache()
def get_settings():
    return DocsSettings()


# 配置实例的对象的创建
docs = get_settings()











