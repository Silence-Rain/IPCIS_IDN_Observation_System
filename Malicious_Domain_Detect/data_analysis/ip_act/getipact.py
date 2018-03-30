# -*- coding: utf-8 -*
import urllib2
import json
import readipdt
import calendar
import mkdir
#传入域名ip字典地址和要查询的月份，将查到的ip活动信息写入到文件夹
def getIpact(addr,month):
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
