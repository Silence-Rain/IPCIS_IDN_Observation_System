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

def active_degree(data):
	res = formatter(data)
	ret = []
	for item in res:
		temp = item
		temp["active"] = active_calc(item)
		ret.append(temp)

	return ret

def active_calc(item):
	return 60

def shannon_entropy(geos):
	return len(geos)