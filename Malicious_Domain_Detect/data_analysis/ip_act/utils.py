# -*- coding: utf-8 -*
import time
import math
import json
import io
import calendar
import urllib2

def standard2timestamp(str_time):
	tm = time.strptime(str_time, '%d-%b-%Y')
	return int(time.mktime(tm))

def timestamp2diff(int_time):
	y = int(math.floor(int_time / 31536000))
	m = int(math.floor((int_time - 31536000 * y) / 2592000))
	d = int(math.floor((int_time - 31536000 * y - 2592000 * m) / 86400))

	return "%s-%s-%s" % (y, m, d)
    
def mkdir(path):            #创建文件夹
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("/")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
 
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

def readIpdt(addr):       #传入文件地址返回域名ip字典
    content = None
    dict={}
    with io.open(addr, 'r', encoding='utf-8') as file:
         content = eval(file.read())

    
    return content
    

def getIpact(addr,month):               #传入域名ip字典地址和要查询的月份，将查到的ip活动信息写入到文件夹
    data=readipdt.readIpdt(addr)
    daofmo=calendar.monthrange(2018,month)[1]

    for key,value in data.items():
        print key,value  
        if len(value):
            #创建活动记录保存目录
            savepath='/home/lzhang/SRTP_DNS/ipact/'+key
            mkdir.mkdir(savepath)
            
            for i in range(daofmo):
                #通过url抓取Ip活动记录
                url ="http://211.65.197.210:8080/IPCIS/activityDatabase?IpSets="+value[0]+":32&TableName=2018-"+str(month)+"-"+str(i)+"&Mode=2"  
                response = urllib2.urlopen(url)   
                html = response.read()  
                mystr = html.decode("utf8")  
                response.close()
                
                if(mystr!="{}"):
                    #将查到的ip活动记录写入到文件夹
                    file = open(savepath+'/'+str(i)+'of'+str(month)+'.txt','w') 
                    file.write(mystr) 
                    file.close()