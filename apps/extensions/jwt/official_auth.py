# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 12:12
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------

from datetime import timedelta, datetime
from typing import Optional
# jwt库
from jose import jwt, JWTError
# token 路由
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from apps.config.docs_conf import docs
from apps.config.auth_conf import auth as auth_conf
# hash 密码库-python-jose
# passlib[bcrypt]
from passlib.context import CryptContext

# 定义密码使用的加密的方式，deprecated是否废弃
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 指定生成token 的路由路径---登入系统获取授权码的路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=docs.API_V1_STR + "/login")


class OfficialAuth():

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """验证密码与hash密码"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        # 指定秘钥和算法模型
        encoded_jwt = jwt.encode(to_encode, auth_conf.JWT_SECRET_KEY, algorithm=auth_conf.JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        # 自定义的认证检测
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, auth_conf.JWT_SECRET_KEY, algorithms=[auth_conf.JWT_ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # 用户信息的查询
        # doctor = await models.User.get(username=username)
        user = {
            'username': 'xiaozhongtongxue'
        }
        if user is None:
            raise credentials_exception
        return user











