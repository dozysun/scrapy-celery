#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from sqlalchemy import orm,Column
from sqlalchemy.types import String,INTEGER,DATETIME,TEXT,DateTime,Boolean,Integer

from base_mod import Base
from datetime import  datetime

class Community(Base):
    __tablename__ = 'community'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(128))
    address = Column(String(128))
    area = Column(INTEGER)
    city = Column(INTEGER)
    province = Column(INTEGER)

    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=0)

class CommunityALL(Base):
    __tablename__ = 'community_all'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(128))
    address = Column(String(128))
    ori_address = Column(String(128))
    area = Column(INTEGER)
    city = Column(INTEGER)
    province = Column(INTEGER)
    city_code = Column(String(128)) #城市代码
    link = Column(String(128)) #58链接
    lng = Column(String(128)) #经度
    lat = Column(String(128)) #纬度
    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=0)

class CommunityALLBackup(Base):
    __tablename__ = 'community_all_backup'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(128))
    address = Column(String(128))
    ori_address = Column(String(128))
    area = Column(INTEGER)
    city = Column(INTEGER)
    province = Column(INTEGER)
    city_code = Column(String(128)) #城市代码
    link = Column(String(128)) #58链接
    lng = Column(String(128)) #经度
    lat = Column(String(128)) #纬度
    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=0)

class CommunityTest(Base):
    __tablename__ = 'communityTest'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(128))
    address = Column(String(128))
    area = Column(INTEGER)
    city = Column(INTEGER)
    province = Column(INTEGER)

    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=0)

class CompanyDianPing(Base):
    __tablename__ = 'company_dianping'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(128))
    area = Column(String(128))
    address = Column(String(256))
    phone = Column(String(128))
    qq = Column(String(128))
    desc = Column(String(2048))

    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=0)


class CompanyDianPingNew(Base):
    __tablename__ = 'company_dianping_new'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(128))
    city = Column(String(128))
    area = Column(String(128))
    address = Column(String(256))
    phone = Column(String(128))
    photo = Column(String(256))
    qq = Column(String(128))
    desc = Column(String(2048))

    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=0)


class Area(Base):
    """
        区域信息
    """
    __tablename__ = 'area'

    id = Column(Integer, primary_key=True)
    area_id = Column(Integer)
    area_name = Column(String(128))                 #区域名称
    father = Column(Integer)
    gmt_created = Column(DateTime,default=datetime.now())
    gmt_modified = Column(DateTime,default=datetime.now())
    deleted = Column(Boolean,default=0)

    def to_dict(self):
        dic = {}
        dic["area_id"] = self.area_id
        dic["city_id"] = self.father
        dic["area_name"] = self.area_name
        return dic

class City(Base):
    """
    城市信息
    """
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String(128))                 #城市名称
    #zip_code = Column(String(10))
    father = Column(Integer)

    gmt_created = Column(DateTime,default=datetime.now())
    gmt_modified = Column(DateTime,default=datetime.now())
    deleted = Column(Boolean,default=0)

    def to_dict(self):
        dic = {}
        dic["province_id"] = self.father
        dic["city_id"] = self.city_id
        dic["city_name"] = self.city_name
        return dic

class Province(Base):
    """
        省份信息
    """
    __tablename__ = 'province'

    id = Column(Integer, primary_key=True)
    province_id = Column(Integer)
    province_name = Column(String(128))                 #省份名称
    gmt_created = Column(DateTime,default=datetime.now())
    gmt_modified = Column(DateTime,default=datetime.now())
    deleted = Column(Boolean,default=0)

    def to_dict(self):
        dic = {}
        dic["province_id"] = self.province_id
        dic["province_name"] = self.province_name
        return dic

class CityLink58(Base):
    """
    城市信息
    """
    __tablename__ = 'city_link_58'

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String(128))                 #城市名称
    province_id = Column(Integer)
    province_name = Column(String(128))                 #省名称
    code = Column(String(128))                                              #城市代码
    link = Column(String(128))
    gmt_created = Column(DateTime,default=datetime.now())
    gmt_modified = Column(DateTime,default=datetime.now())
    deleted = Column(Boolean,default=0)
