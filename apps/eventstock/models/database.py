# --------------
# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2022/3/5 19:39
# @project_name : ybjrun
# @author :	pujen_yuan
# ------------


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apps.config.config import dbconf

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{dbconf.DB_PASS}@{dbconf.DB_HOST}/{dbconf.DB_NAME}?charset=utf8mb4"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()









