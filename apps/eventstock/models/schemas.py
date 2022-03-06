# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 19:50
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------


from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True









