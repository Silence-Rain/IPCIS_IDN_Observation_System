# -*- coding: utf-8 -*
import json
import io
#传入地址，返回字典内容——域名：ip
def readIpdt(addr):
    content = None
    dict={}
    with io.open(addr, 'r', encoding='utf-8') as file:
         content = eval(file.read())

    
    return content
            
