# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 19:49
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


# 定义 Original_data 类
class OriginalData(Base):

    __tablename__ = 'original_data'  # 定义表名
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")








