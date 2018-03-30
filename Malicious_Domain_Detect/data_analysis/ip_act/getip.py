# !/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb
import os  
import socket
import struct

file = open('./3mths.txt') 

#获取域名列表
name_list = []  
for  line in  file.readlines(): 
         name_list.extend(line.split("=")[1].split(",")[0:-1:1])

#去除列表中元素的空格
for i in range(len(name_list)):
     name_list[i]=name_list[i].strip()   
     
#打印测试
#for  ip in  name_list:
#        print (ip)

file.close()

#连接数据库
conn = MySQLdb.connect(host='127.0.0.1',port= 3307,user = 'root',passwd='rootofmysql',db='IPCIS_DNS_DB') #db：库名

#创建游标
cur = conn.cursor()

#ip字典
ip_dic = {}

# SQL 查询语句
for name in name_list :
   sql = "select ip from resolved_ip where domain_name='"+name+"';"
   #执行SQL语句
   cur.execute(sql)
   
   
   #fetchall:获取ip的数据
   ip = cur.fetchall()
   if len(ip) !=0:
       ip = list(ip[0])
   else:
       ip = []
       
   for i in range(len(ip)):
       ip[i] = socket.inet_ntoa(struct.pack('!I',ip[i]))
       
   ip_dic[name]=ip


#保存ip字典
file = open('./ipdata.txt','w') 
file.write(str(ip_dic))  
file.close()  


#提交
conn.commit()

#关闭指针对象
cur.close()

#关闭连接对象
conn.close()