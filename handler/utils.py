import time

def standard2timestamp(str_time):
	tm = time.strptime(str_time, '%Y-%m-%d')
	return int(time.mktime(tm))

def timestamp2standard(int_time):
	tm = time.localtime(int_time)
	return time.strftime('%Y-%m-%d', tm)