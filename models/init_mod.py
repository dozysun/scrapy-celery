#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from sqlalchemy import create_engine

from models.base_mod import Base
from settings import ENGINE
from models.qa_mod import *

if __name__ == '__main__':
    engine = create_engine(ENGINE,echo=True)
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
