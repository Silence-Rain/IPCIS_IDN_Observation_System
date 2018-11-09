#!coding=utf8

from IPy import *
from config import *
import requests
import time
import json

class GeoDistributionModel(object):

	# 获取指定语种IDN的解析IP地理位置（从文件读取）
	async def get_all_geo_distribution(self, lang):
		ret = {"self":[]}
		temp = []
		with open("data/res.dat", "r") as f:
			temp = eval(f.readline())

		# 根据传入参数过滤语种
		if lang != "全部语种":
			for item in temp:
				if item["lang"] == lang:
					ret["self"].append(item)
		else:
			ret["self"] = temp

		return ret

	# 获取某个域名，在最近几天内的通信对端解析IP地理位置（向流记录库中查询）
	async def get_geo_distribution(self, ips, length):
		ret = {"self": [], "opposite": []}
		opposite_ips = []

		# 取有记录的日期里，最近length天
		proxy = IPCIS_CONFIG
		url_tables = "http://211.65.197.210:8080/IPCIS/activityDatabase/?Mode=3"
		r_tables = requests.get(url_tables, proxies=proxy)
		tables = r_tables.json()["tables"][-length:]

		for date in tables:
			for ip in ips:
				url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=1" % (ip, date)
				r = requests.get(url, proxies=proxy)
				try:
					res = r.json()[ip+":32"]
				except:
					continue

				# 只统计以目标IP为宿地址的流记录
				item = res[1]
				self_flag = False
				if len(item) == 0:
					continue
				# 获得解析IP经纬度，管理归属，地理位置，只记录一次
				if not self_flag:
					self_flag = True
					target_pos = item[0].split(" ")[13:]
					auth_location = " ".join(target_pos).split("$")
					lnglat = auth_location[0].split(" ")

					ret["self"].append({
						"ip": ip,
						"location": auth_location[2],
						"auth": auth_location[1],
						"lng": float(lnglat[0]),
						"lat": float(lnglat[1])
						})

				# 获得对端IP经纬度，地理位置，管理归属
				for i in item[1:]:
					temp = i.split("$")
					ip1 = temp[0].split(" ")[0]
					ip2 = temp[0].split(" ")[1]
					opposite_ip = ip1 if ip1 != ip else ip2

					# 去除几天内重复出现的IP
					if opposite_ip not in opposite_ips:
						opposite_ips.append(opposite_ip)
						opposite_ip_auth = temp[5]
						opposite_ip_location = temp[7]
						opposite_pos = temp[8].split(" ")
						ret["opposite"].append({
							"ip": opposite_ip,
							"auth": opposite_ip_auth,
							"location": opposite_ip_location,
							"lng": float(opposite_pos[1]),
							"lat": float(opposite_pos[2])
							})

		return ret
	