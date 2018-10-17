#!coding=utf8

from IPy import *
import requests
import datetime
import json

class GeoDistributionModel(object):

	async def get_geo_distribution(self, ips):
		ret = {"self": [], "opposite": []}
		now = datetime.date.today()
		for ip in ips:
			url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=1" % (ip, "2018-10-17")
			proxy = {"http": "http://yunyang:yangyun123@202.112.23.167:8080"}
			r = requests.get(url, proxies=proxy)
			res = r.json()[ip+":32"]

			for item in res:
				if len(item) == 0:
					continue

				# 获得解析IP经纬度
				target_pos = item[0].split(" ")[-2:]
				ret["self"].append({
					"ip": ip,
					"lng": float(target_pos[0]),
					"lat": float(target_pos[1])
					})

				# 获得对端IP经纬度，地理位置，管理归属
				for i in item[1:]:
					temp = i.split("$")
					ip1 = temp[0].split(" ")[0]
					ip2 = temp[0].split(" ")[1]
					opposite_ip = ip1 if ip1 != ip else ip2
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
	