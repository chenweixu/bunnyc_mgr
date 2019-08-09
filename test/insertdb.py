#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Email: chenwx716@163.com
# DateTime: 2019-04-27 16:32:13
__author__ = 'chenwx'
import pymysql

db_conn = pymysql.connect(
    host='127.0.0.1',port=3306,user='bunnyc',passwd='passw8rd',
    db='bunnyc',charset='utf-8',connect_timeout=4,
    )
curs = db_conn.cursor()

sql = "insert into t_host_cpu(\
ctime,ip,cpu,cpu_user_rate,cpu_nice_rate,cpu_system_rate,cpu_idle_rate,cpu_iowait_rate,cpu_irq_rate,cpu_softirq_rate,\
ld_1,ld_2,ld_3,proc_run,proc_sub) values (\
'%s','%s','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%f','%d','%d')"  % (\
data.get('ctime'),
data.get('ip'),
data.get('cpu_rate'),
data.get('cpu_user_rate'),
data.get('cpu_nice_rate'),
data.get('cpu_system_rate'),
data.get('cpu_idle_rate'),
data.get('cpu_iowait_rate'),
data.get('cpu_irq_rate'),
data.get('cpu_softirq_rate'),
data.get('ld_1'),
data.get('ld_5'),
data.get('ld_15'),
data.get('proc_run'),
data.get('proc_sum')
)


curs.execute(sql)
db_conn.commit()

curs.close()
db_conn.close()
