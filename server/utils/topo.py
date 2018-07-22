# 将原始数据转换为日期-ip活动的字典
# 输入：[[ip_src, ip_dst, count, date], ...]
# 输出：{date: (ip_src, ip_dst), ...}
def raw2date_dict(data):
	keys = []
	values = []

	for item in data:
		# 判断当前日期是否已经作为key
		if item[-1] in keys:
			values[keys.index(item[-1])].append(tuple(item[:-2]))
		else:
			keys.append(item[-1])
			values.append([tuple(item[:-2])])

	return dict(zip(keys, values))

# 将原始数据转换为ip-累计活动量的字典
# 输入：[[ip_src, ip_dst, count, date], ...]
# 输出：{ip: count, ...}
def raw2count(data):
	ret = {}

	for item in data:
		# 判断当前日期是否已经作为key
		if item[-1] not in ret:
			ret[item[-1]] = [{item[0]:0}]
		# 添加目的ip计数
		ret[item[-1]].append({item[1]:item[2]})
		# 源ip计数累计
		ret[item[-1]][0][item[0]] += item[2]

	return flatten_dict(ret)

# 将每天活动量字典按日期展开，得到ip与对应累计活动量
# 输入：{date: [{ip: count}, ...], ...}
# 输出：{ip: count, ...}
def flatten_dict(data):
	ret = {}

	for date in data.values():
		for item in date:
			ip = list(item.keys())[0]
			if ip not in ret:
				ret[ip] = item[ip]
			else:
				ret[ip] += item[ip]

	return ret

# 拓扑图节点构造函数
def node_constructor(nodes, counts):
	ret = []
	for index, item in enumerate(nodes):
		ret.append({"id": index, "name": item, "count": counts[item]})

	return ret

# 拓扑图边构造函数
def link_constructor(nodes, links):
	ret = []
	for item in links:
		ret.append({"source": nodes.index(item[0]), "target": nodes.index(item[1])})

	return ret

# 获取ip活动的稳定拓扑结构
def steady_topo(data, days):
	dic = raw2date_dict(data)		# 日期-ip活动字典
	count_map = raw2count(data)		# ip-活动量字典
	raw = {}
	# 对每天的ip活动取交集
	for index, date in enumerate(dic.keys()):
		for item in dic[date]:
			if str(item) not in raw:
				raw[str(item)] = 1
			else:
				raw[str(item)] += 1

	# 若一对活动出现次数大于等于days，算入稳定拓扑
	intersect = set()
	for key, value in raw.items():
		if value >= days:
			intersect.add(eval(key))

	# 计算交集节点集合
	node_set = set()
	for item in intersect:
		node_set.update(item)
	nodes_raw = list(node_set)
	# 构造拓扑图节点和边
	nodes = node_constructor(nodes_raw, count_map)
	links = link_constructor(nodes_raw, list(intersect))

	return {"nodes": nodes, "links": links}

# 获取ip活动的最大拓扑结构
def max_topo(data):
	dic = raw2date_dict(data)		# 日期-ip活动字典
	count_map = raw2count(data)		# ip-活动量字典
	union = set()
	# 对每天的ip活动取并集
	for index, date in enumerate(dic.keys()):
		temp = set()
		for item in dic[date]:
			temp.add(tuple(item))

		if index == 0:
			union.update(temp)
		else:
			union = union | temp

	# 计算并集节点集合
	node_set = set()
	for item in union:
		node_set.update(item)
	nodes_raw = list(node_set)
	# 构造拓扑图节点和边
	nodes = node_constructor(nodes_raw, count_map)
	links = link_constructor(nodes_raw, list(union))

	return {"nodes": nodes, "links": links}
