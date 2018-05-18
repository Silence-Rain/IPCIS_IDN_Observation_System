def raw2date_dict(data):
	keys = []
	values = []
	for item in data:
		if item[-1] in keys:
			values[keys.index(item[-1])].append(tuple(item[:-2]))
		else:
			keys.append(item[-1])
			values.append([tuple(item[:-2])])

	return dict(zip(keys, values))

def node_constructor(nodes):
	ret = []
	for index, item in enumerate(nodes):
		ret.append({"id": index, "name": item})

	return ret

def link_constructor(nodes, links):
	ret = []
	for item in links:
		ret.append({"source": nodes.index(item[0]), "target": nodes.index(item[1])})

	return ret

def steady_topo(data):
	dic = raw2date_dict(data)
	intersect = set()
	for index, date in enumerate(dic.keys()):
		for item in dic[date]:
			if index == 0:
				intersect.add(tuple(item))
			else:
				temp = set()
				temp.add(tuple(item))
				intersect = intersect & temp

	node_set = set()
	for item in intersect:
		node_set.update(item)
	nodes_raw = list(node_set)
	nodes = node_constructor(nodes_raw)
	links = link_constructor(nodes_raw, list(intersect))

	return {"nodes": nodes, "links": links}

def max_topo(data):
	dic = raw2date_dict(data)
	intersect = set()
	for index, date in enumerate(dic.keys()):
		for item in dic[date]:
			if index == 0:
				intersect.add(tuple(item))
			else:
				temp = set()
				temp.add(tuple(item))
				intersect = intersect | temp

	node_set = set()
	for item in intersect:
		node_set.update(item)
	nodes_raw = list(node_set)
	nodes = node_constructor(nodes_raw)
	links = link_constructor(nodes_raw, list(intersect))

	return {"nodes": nodes, "links": links}