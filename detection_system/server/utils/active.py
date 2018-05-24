import math

# 格式化数据
# 输入：[{
#		"ip": ip, 
# 		"count": [counts], 
# 		"opposite_ip": {date: [ips], ...}, 
# 		"ip_geo": {date: [lnglats], ...}
# 		}, ...]
# 输出：[{
#		"ip": ip, 
# 		"count": [counts], 
# 		"opposite_ip_count": [ip_counts], 
# 		"ip_geo": [entropys]
# 		}, ...]
def formatter(data):
	ret = []
	for item in data:
		opposite_ip_count = []
		ip_geo = []
		for value in item["opposite_ip"].values():
			opposite_ip_count.append(len(value))

		for value in item["ip_geo"].values():
			ip_geo.append(shannon_entropy(value))

		ret.append({"ip":item["ip"], "count":item["count"], 
			"opposite_ip_count":opposite_ip_count, "ip_geo":ip_geo})

	return ret

# 在原始数据上添加active字段
def active_degree(data):
	res = formatter(data)
	ret = []
	for item in res:
		temp = item
		temp["active"] = active_calc(item)
		ret.append(temp)

	return ret

# 计算域名活跃度
def active_calc(item):
	return 60

# 计算ip地理分布香农熵
def shannon_entropy(geos):
	raw = [x.split("-")[0] for x in geos]
	prob_raw = {}
	for item in raw:
		if item in prob_raw:
			prob_raw[item] += 1
		else:
			prob_raw[item] = 1

	total = len(raw)
	prob = [x / total for x in prob_raw.values()]

	entropy = 0
	for item in prob:
		entropy -= item * math.log2(item)

	return round(entropy,6)
