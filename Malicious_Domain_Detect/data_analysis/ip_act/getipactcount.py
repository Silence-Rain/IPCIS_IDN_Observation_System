# !/usr/bin/env python
# -*- coding:utf-8 -*-
import glob

#传入文件夹地址，返回字典内容——文件名：通讯记录行数
def getIpactCount(addr):
    data={}
    read_files=glob.glob(addr)

    for i in read_files:
        with open(i,'r') as infile:
            ipact=infile.readlines()
        count=len(ipact)
        data[i.split("\\")[-1].split(".")[0]]=count
    return data



