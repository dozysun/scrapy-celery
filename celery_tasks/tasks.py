#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import

__author__ = 'dozy-sun'

import time

from celery_tasks.base import DatabaseTasks
from celery_tasks.celery import app
from models.qa_mod import *
# from services.message.message_service import MessageService

# msg_db = MessageService()

@app.task
def sleep(seconds):
    time.sleep(3600)

@app.task
def sleep(seconds):
    time.sleep(float(seconds))
    print seconds
    return seconds

@app.task(base=DatabaseTasks)
def sqltest(table):
    sqltest.db.execute('insert into users(`nick`) values ("%s")' % table)
    sqltest.db.commit()

@app.task
def add(x, y):
    print x+y
    return x + y

@app.task(base=DatabaseTasks)
def create_community(name,address):
    name = [n.strip() for n in name if n.strip()]
    details = zip(name, address)
    create_community.db.execute(
        Community.__table__.insert(),[{
                                          'name':n[0],
                                          'address':(n[1].split(u'】')[-1].strip() if '...' not in n[1] else u'、'.join(n[1].split(u'】')[-1].strip().split(u'、' if u'、' in n[1] else u'，' if u'，' in n[1] else u'（' if u'（' in n[1] else u' ')[0:-1])  if len(n[1].split(u'】')[-1].strip().split(u'、' if u'、' in n[1] else u'，' if u'，' in n[1] else u'（' if u'（' in n[1] else u' '))>1 else n[1].split(u'】')[-1].strip().split(u' ')[0] ).strip() ,
                                          'area': create_community.db.query(Area.id).filter(Area.area_name.like('%s%%' % n[1][1:3]),Area.id.between(719,735) ,Area.deleted==0).scalar()
                                        } for n in details if not create_community.db.query(Community.id).filter(Community.address.like('%%%s%%' % n[1].split(u'】')[-1].strip().split(u'、')[0].split(u'，')[0].split(u'（')[0].split(u' ')[0])).first()]
    )
    sqltest.db.commit()


@app.task(base=DatabaseTasks)
def create_community_all(address_list, city=73, province=9, city_code = 'sh'):
    create_community.db.execute(
        CommunityALL.__table__.insert(),[{
                                          'name':n[0],
                                          'ori_address': n[1],
                                          'address':(n[1].split(u'】')[-1].strip() if '...' not in n[1] else u'、'.join(n[1].split(u'】')[-1].strip().split(u'、' if u'、' in n[1] else u'，' if u'，' in n[1] else u'（' if u'（' in n[1] else u' ')[0:-1])  if len(n[1].split(u'】')[-1].strip().split(u'、' if u'、' in n[1] else u'，' if u'，' in n[1] else u'（' if u'（' in n[1] else u' '))>1 else n[1].split(u'】')[-1].strip().split(u' ')[0] ).strip() ,
                                          'link': n[2],
                                          'area': create_community_all.db.query(Area.id).filter(Area.area_name.like('%s%%' % n[1][1:3]),Area.father==city,Area.deleted==0).scalar(),
                                          'city': city,
                                          'province':province,
                                          'city_code': city_code
                                        } for n in address_list ]
    )
    create_community_all.db.commit()


@app.task(base=DatabaseTasks)
def create_community_test(name,address):
    name = [n.strip() for n in name if n.strip()]
    details = zip(name, address)
    create_community.db.execute(
        CommunityTest.__table__.insert(),[{
                                          'name':n[0], 'address':n[1]
                                        } for n in details ]
    )
    sqltest.db.commit()


@app.task(base=DatabaseTasks)
def create_company_test(**kwargs):
    company = CompanyDianPing()
    company.name = kwargs['title'][0]
    company.area = kwargs['area'][0] if kwargs['area'] else ''
    company.address = kwargs['addr'][0] if kwargs['addr'] else ''
    company.phone = kwargs['phone'][0] if kwargs['phone'] else ''
    company.qq = kwargs['phone'][1] if len(kwargs['phone']) > 1 else ''
    if kwargs['desc']:
        desc = ','.join(kwargs['desc'])
        company.desc = desc
    create_company_test.db.add(company)
    create_company_test.db.commit()

@app.task(base=DatabaseTasks)
def create_company_from_dianping_all(**kwargs):
    company = CompanyDianPingNew()
    company.city = kwargs['city'][0].replace(u'站', '') if kwargs['city'] else ''
    company.name = kwargs['title'][0] if kwargs['title'] else ''
    company.area = kwargs['area'][0] if kwargs['area'] else ''
    company.address = kwargs['addr'][0] if kwargs['addr'] else ''
    company.phone = kwargs['phone'][0] if kwargs['phone'] else ''
    company.photo = kwargs['photo'][0] if kwargs['photo'] else ''
    company.qq = kwargs['phone'][1] if len(kwargs['phone']) > 1 else ''
    if kwargs['desc']:
        desc = ','.join(kwargs['desc'])
        company.desc = desc
    create_company_test.db.add(company)
    create_company_test.db.commit()


# if __name__ =='__main__':
#     area_list = create_community.db.query(Area.name,Area.id).filter(Area.deleted==0).all()
#     area_dict = dict(*area_list)
#     print area_dict


# @app.task(base=DatabaseTasks)
# def create_user_message(**kwargs):
#     print 'user_message 20'
#     print kwargs
#     msg_db.set_db(create_user_message.db)
#     kwargs['msg_id'] = msg_db.create_msg_text(**kwargs)
#     if kwargs.get('info_type') or kwargs.get('text_type') and kwargs['text_type'] == 'private':
#         msg_db.create_msg_info(**kwargs)
#     create_user_message.db.close()
#     return True
