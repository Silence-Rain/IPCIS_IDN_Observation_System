import io
import requests
from IPy import *

def get_idns_flow_record():

	domains = []		# 域名列表
	ips = []			# 解析IP列表
	lang_map = {}		# 域名-语种映射
	records = []		# IP活动记录列表
	cur_ips = []		# IP去重
	rs = []				# 最终结果

	# 读取原始idn数据
	with io.open("minority.txt", "r", encoding="utf8") as f:
		for line in f.readlines():
			temp = line.split(",")
			domains.append(temp[0])
			ips.append(str(IP(temp[1])))
			lang_map[temp[0]] = temp[2].strip()

	# 从流记录库中获取原始流记录
	for index,ip in enumerate(ips):
		print(index)
		url = "http://211.65.197.210:8080/IPCIS/activityDatabase/?IpSets=%s:32&TableName=%s&Mode=1" % (ip, "2018-10-17")
		proxy = {"http": "http://yunyang:yangyun123@202.112.23.167:8080"}
		r = requests.get(url, proxies=proxy)
		res = r.json()[ip+":32"]
		item = res[1]

		if len(item) == 0:
			continue
		# 获得解析IP经纬度，归属，地址
		target_pos = item[0].split(" ")[13:]
		auth_location = " ".join(target_pos).split("$")
		lnglat = auth_location[0].split(" ")

		records.append({
			"domain": domains[index],
			"ip": ip,
			"location": auth_location[2],
			"auth": auth_location[1],
			"lng": float(lnglat[0]),
			"lat": float(lnglat[1])
			})

	# IP去重
	for item in records:
		if item["ip"] not in cur_ips:
			cur_ips.append(item["ip"])
			rs.append(item)

	with io.open("res.dat", "w") as f:
		f.write(str(rs))
