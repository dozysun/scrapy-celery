#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
from sqlalchemy.orm.interfaces import MapperExtension
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Column, Integer, DateTime, Boolean
from datetime import datetime
# from packages.date_pack import now


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(Integer, primary_key=True)
    gmt_created = Column(DateTime, default=datetime.now())
    gmt_modified = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, default=False)

class ModelMixin(object):

    @classmethod
    def get_by_id(cls, session, id, columns=None, lock_mode=None):
        if hasattr(cls, 'id'):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(cls.id == id)
            if scalar:
                return query.scalar()
            return query.first()
        return None

    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            if hasattr(cls, 'deleted'):
                query = session.query(cls).filter(cls.deleted==0)
            else:
                query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()


    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()


    @classmethod
    def exist(cls,session,**kargs):

        query = session.query(func.count('*')).select_from(cls)
        for key in kargs.keys():
            key=kargs.get(key)
            if hasattr(cls, key):
                query = query.filter_by()
        # if hasattr(cls, 'id'):
        #    .filter(cls.id == id)
            # if lock_mode:
            #     query = query.with_lockmode(lock_mode)
        return query.scalar() > 0
        #return False

    @classmethod
    def set_attr(cls, session, id, attr, value):
        if hasattr(cls, 'id'):
            session.query(cls).filter(cls.id == id).update({
                attr: value,
                'gmt_modified':datetime.now()
            })
            session.commit()


    @classmethod
    def set_attrs(cls, session, id, **attrs):
        if hasattr(cls, 'id'):
            attrs['gmt_modified'] = datetime.now()
            session.query(cls).filter(cls.id == id).update(attrs)
            session.commit()


Base = declarative_base(cls=ModelMixin)


class DataUpdateExtension(MapperExtension):

    def before_update(self, mapper, connection,instance):
        print 'before update obj--------------------'
        if hasattr(instance,'gmt_modified'):
            instance.gmt_modified = datetime.now()


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

