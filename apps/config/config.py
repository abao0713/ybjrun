# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 10:57
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------
import os
from functools import lru_cache
from pydantic import BaseSettings,AnyUrl
import pprint
import secrets
from typing import List

pp = pprint.PrettyPrinter(indent=4)


class AppsSettings(BaseSettings):
    #用户的鉴权配置
    pass
class AuthUrlSettings(BaseSettings):
    # token相关-加密算法
    JWT_ALGORITHM: str = "HS256"  #
    # 秘钥生成
    # JWT_SECRET_KEY: str = secrets.token_urlsafe(32)  # 随机生成的base64位字符串
    JWT_SECRET_KEY: str = '09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7'
    # token配置的有效期
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # token的时效 3 天 = 60 * 24 * 3
    JWT_REFRESH_EXPIRES_DAYS: int = 1

    # 跨域设置
    ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'

    ADMIN_WHILE_ROUTE = [
        # '/sys/doctor/logout',
        '/5gmsg/sys/doctor/login',
        '/nw/sys/doctor/login',
        '/',
        '/check',
        '/check23',
        '/jcg_admin/api/v1/login',
        '/websocket/1',
        '/openapi_url',
        '/nw/sys/doctor/login',
        '/nw/sys/doctor/loginceshi'
    ]

class DatabaseSettings(BaseSettings):
    DEPLOY_HOST: str = '0.0.0.0'
    DEPLOY_PORT: int = 8888
    DEPLOY_DEBUG: bool = False
    DEPLOY_RELOAD: bool = False
    DEPLOY_ACCESS_LOG: bool = False

    # 要连接的数据库名称
    DB_NAME = 'hanxuanyuyue'
    # 数据库的端口
    DB_PROT = 5432
    # 连接数据库的用户
    DB_USER = 'postgres'
    # 连接的数据库的密码
    DB_PASS = '123456'
    # 要连接的数据库的HOST
    DB_HOST = 'localhost'


    DB_MAX_CONNECTIONS = 60
    DB_STALE_TIMEOUT = 300
    DB_TIMEOUT = 20

class RabbitSettings(BaseSettings):
    #  没有值的情况下的默认值--默认情况下读取的环境变量的值
    # 链接用户名
    RABBIT_USERNAME: str = 'guest'
    # 链接密码
    RABBIT_PASSWORD: str = 'guest'
    # 链接的主机
    RABBIT_HOST: str = 'localhost'
    # 链接端口
    RABBIT_PORT: int = 5672
    # 要链接租户空间名称
    VIRTUAL_HOST: str = 'xiaozhong'
    # 心跳检测
    RABBIT_HEARTBEAT = 5

class RedisSettings(BaseSettings):
    #  没有值的情况下的默认值--默认情况下读取的环境变量的值
    HOST: str = '127.0.0.1'
    PORT: int = 6379
    PASSWORD:str =''
    DEPLOY_DEBUG: bool = False
    DEPLOY_RELOAD: bool = False
    DEPLOY_ACCESS_LOG: bool = False

    # redis://:root12345@127.0.0.1:6379/0?encoding=utf-8
    # 下面这个其实不需要这么操作，默认会自己去读取环境变量的值
    redis_url: AnyUrl = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0?encoding=utf-8")
    redis_password: str = os.getenv("REDIS_PASSWORD", "")
    redis_db: int = int(os.getenv("REDIS_DB", "0"))

    # 哨兵机制的链接的配置
    use_redis_sentinel: bool = (
        True if os.getenv("REDIS_USE_SENTINEL", "0") == "1" else False
    )
    redis_sentinel_port: int = int(os.getenv("REDIS_SENTINEL_PORT", "26379"))
    redis_sentinel_url: str = os.getenv("REDIS_SENTINEL_URL", "")
    redis_sentinel_password: str = os.getenv("REDIS_SENTINEL_PASSWORD", "")
    redis_sentinel_master_name: str = os.getenv(
        "REDIS_SENTINEL_MASTER_NAME", "molmaster"
    )

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



# 一一获取类对象
@lru_cache()
def get_auth_settings():
    return AuthUrlSettings()


@lru_cache()
def get_db_settings():
    return DatabaseSettings()


@lru_cache()
def get_mq_settings():
    return RabbitSettings()


@lru_cache()
def get_redis_settings():
    return RedisSettings()


@lru_cache()
def get_doc_settings():
    return DocsSettings()

auth = get_auth_settings()
pgconf = get_db_settings()
# rabbitconf = get_mq_settings()
redisconf = get_redis_settings()
docsconf = get_doc_settings()






